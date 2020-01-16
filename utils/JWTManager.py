import datetime

import jwt
from jwt import ExpiredSignatureError
from authentication.models import User
from janatar_kolom.settings import SECRET_KEY


class JWTManager:
    algorithms = 'HS256'
    payload = {}
    exception = None
    token = None

    def generate_token(self, payload: dict):
        self.payload = payload
        self.token = jwt.encode(payload, SECRET_KEY, algorithm=self.algorithms).decode('utf-8')
        return self.token

    def validate_token(self, cypher: str, leeway: datetime = 0):
        self.token = cypher
        try:
            self.payload = jwt.decode(cypher, SECRET_KEY, algorithms=self.algorithms)
            return True
        except Exception as e:
            self.exception = e
            return False

    def get_payload(self):
        return self.payload

    def get_exception(self):
        return self.exception

    def is_signature_expired(self):
        return True if type(self.exception) is ExpiredSignatureError else False

    def get_user(self):
        try:
            return User.objects.get(user_id=self.payload['user_id'])
        except:
            return None

    def is_refresh_token(self):
        try:
            return True if self.payload['purpose'] == "refresh" else False
        except KeyError as e:
            return False

    def update_token_if_required(self):
        expiry = self.payload['exp']
        expiry_date = datetime.datetime(expiry)
        current_date = datetime.now()
        diff = current_date - expiry_date
        diff_div = divmod(diff.days * 86400 + diff.seconds, 60)
        mins = diff_div[0]
        if mins < 5:
            # Generate new expiry date
            self.payload['exp'] = datetime.datetime.now() + datetime.timedelta(days=30)
            self.token = self.generate_token(self.payload)
        return self.token
