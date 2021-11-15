from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from authentication.Decorators.AuthorizationValidator import unauthorized_user_only, require_services_enabled_permission
from authentication.models import User
from utils.JWTManager import JWTManager
from utils.JsonRequestParserMiddleware import JsonRequestParser

decorators = [csrf_exempt, require_services_enabled_permission]


@method_decorator(decorators, name='dispatch')
class Login(View):

    model = User

    @method_decorator(decorator=unauthorized_user_only, name='dispatch')
    def post(self, request, *args, **kwargs):
        """ Login User and Generate New Access Token """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        token = None
        ref_token = None
        print(arguments)
        try:
            email = arguments.get('email')
            password = arguments.get('password')
        except:
            status = False
            code = 500
            message = "Internal Server Error"
        if status:
            user = authenticate(email=email, password=password)
            if user is not None:
                # Create a session for the user
                login(request, user)
                # Generate JWT access token
                payload = user.serialize()
                payload['exp'] = datetime.now() + timedelta(days=30)
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
                        "refresh_token": ref_token,
                        "redirect": "/adminDashboard" if user.is_administrator() else "/accountInfo",
                        "type": user.user_type
                    }
                ]
            else:
                status = False
                code = 401
                message = "Invalid Login Credentials"
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }
        print("data")
        print(data)
        print("-------")
        print(resp)
        response = JsonResponse(resp, status=code)
        if token is not None:
            response['Authorization'] = "Bearer " + token
            response.set_cookie(
                key="HTTP_AUTHORIZATION",
                value="Bearer " + token,
                expires=refresh_payload["exp"],
                httponly=True
            )
        return response