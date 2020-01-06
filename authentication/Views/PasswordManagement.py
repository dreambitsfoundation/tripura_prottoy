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
class ChangePassword(View):

    model = User

    @method_decorator(decorator=login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        """ Change Password """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        user = request.user
        try:
            old_pass = arguments.get('old')
            new_pass = arguments.get('new')
        except:
            status = False
            code = 500
            message = "Error retrieving request data "
        if status:
            if old_pass == new_pass:
                status = False
                code = 403
                message = "New password cannot be same as Old password"
        if status:
            valid_account = authenticate(email=user.email, password=old_pass)
            if valid_account is not None:
                user.change_password(new_pass)
                user.save()
                message = "Data Updated Successfully"
            else:
                status = False
                code = 403
                message = "Old password do not match"
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }
        return JsonResponse(resp, status=code)