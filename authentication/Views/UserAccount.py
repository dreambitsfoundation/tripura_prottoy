from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from authentication.Decorators.AuthorizationValidator import login_required, admin_only, super_admin_only, \
    require_services_enabled_permission, require_admin_dashboard_enabled_permission, unauthorized_user_only, \
    require_customer_signup_enabled_permission
from authentication.models import SuperAdminSetup, User
from utils.JsonRequestParserMiddleware import JsonRequestParser

decorators = [csrf_exempt, require_services_enabled_permission]


@method_decorator(decorators, name='dispatch')
class UserAccountView(View):

    model = User

    @method_decorator([login_required], name="dispatch")
    def get(self, request, *args, **kwargs):
        """ Returns all the stored permissions """
        all_user = self.model.objects.filter(id=request.user.id)
        if len(all_user):
            user = all_user[0]
            resp = {
                "status": True,
                "code": 200,
                "message": "",
                # "csrf": _get_new_csrf_token(),  # For information purpose only
                "data": [user.serialize()]
            }
        return JsonResponse(resp)

    @method_decorator([require_customer_signup_enabled_permission, unauthorized_user_only], name='dispatch')
    def post(self, request, *args, **kwargs):
        """ Update permissions """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            first_name = arguments.get("first_name")
            last_name = arguments.get("last_name")
            phone_number = arguments.get("phone_number")
            email = arguments.get("email")
            password = arguments.get("password")
            city = arguments.get("city")
            state = arguments.get("state")
        except:
            status = False
            code = 500
            message = "Error extracting information"
        if status:
            existing_user = self.model.objects.filter(phone_number = phone_number)
            if len(existing_user):
                status = False
                code = 403
                message = "User already exist"
            else:
                try:
                    user = self.model()
                    user.create_new(
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        password=password,
                        state=state,
                        city=city,
                        email=email
                    )
                    user.save()
                    message = "Profile saved successfully"
                except:
                    status = False
                    code = 500
                    message = "Operation could not be completed"
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }
        return JsonResponse(resp)

    @method_decorator([login_required], name='dispatch')
    def put(self, request, *args, **kwargs):
        """ Update permissions """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            id = arguments.get("id")
            first_name = arguments.get("first_name")
            last_name = arguments.get("last_name")
            phone_number = arguments.get("phone_number")
            city = arguments.get("city")
            state = arguments.get("state")
        except:
            status = False
            code = 500
            message = "Error extracting information"
        if status:
            user_existance = self.model.ojects.filter(id = int(id))
            if not len(user_existance):
                status = False
                code = 403
                message = "User account not found"
            if status:
                try:
                    user = user_existance[0]
                    user.update(
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        state=state,
                        city=city
                    )
                    user.save()
                except:
                    status = False
                    code = 500
                    message = "User details could not be updated."
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }
        return JsonResponse(resp)