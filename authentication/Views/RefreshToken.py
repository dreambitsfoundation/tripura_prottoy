from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.views import View

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from authentication.Decorators.AuthorizationValidator import login_required, unauthorized_user_only
from authentication.models import User
from utils.JWTManager import JWTManager
from utils.JsonRequestParserMiddleware import JsonRequestParser


@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenView(View):

    model = User

    @method_decorator(decorator=unauthorized_user_only, name='dispatch')
    def post(self, request, *args, **kwargs):
        """ Generated new access token for the refresh token """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        token = None
        ref_token = None
        print(arguments)
        try:
            refresh_token = arguments.get('token')
        except:
            status = False
            code = 500
            message = "Internal Server Error"
        if status:
            # Validate the token
            token_mgr = JWTManager()
            if not (token_mgr.validate_token(refresh_token) and token_mgr.is_refresh_token()):
                status = False
                code = 401
                message = "INVALID REFRESH TOKEN"
        if status:
            user = token_mgr.get_user()
            if user is not None:
                # Generate JWT access token
                payload = user.serialize()
                payload['exp'] = datetime.now() + timedelta(minutes=60)
                token_mgr = JWTManager()
                token = token_mgr.generate_token(payload)
                # Generate JWT Refresh Token
                refresh_payload = {
                    "user_id": payload['user_id'],
                    "purpose": "refresh",
                    "exp": datetime.now() + timedelta(days=30)
                }
                ref_token_mgr = JWTManager()
                ref_token = ref_token_mgr.generate_token(refresh_payload)
                data = [
                    {
                        "access_token": token,
                        "refresh_token": ref_token
                    }
                ]
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }
        return JsonResponse(resp, status=code)
