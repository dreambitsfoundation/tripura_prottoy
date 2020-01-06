from django.views import View
from authentication.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from authentication.Decorators.AuthorizationValidator import login_required, admin_only, standard_user_only, \
    admin_and_org_admin_only
from organisation.models import OrgAccessRequest
from django.http import JsonResponse
from utils.JsonRequestParserMiddleware import JsonRequestParser
from django.db import transaction
from organisation.Models import OrgAccountModel
from django.db import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class OrgRegistrationRequestView(View):
    """ All the requests for Org Account access is accounted here """

    Requests = OrgAccessRequest
    OrgAccount = OrgAccountModel

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        try:
            pending_requests = self.Requests.models.filter(pending=True)
            complete_requests = self.Requests.modes.filter(pending=False)
            data = [
                {
                    "pending": [r.serialize() for r in pending_requests],
                    "complete": [r.serialize() for r in complete_requests]
                }
            ]
        except:
            status = False
            code = 500
            message = "Error fetching results. Contact support."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })

    @method_decorator(decorator=[login_required, standard_user_only], name='dispatch')
    def post(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            company_name = arguments.get("company_name")
        except:
            status = False
            code = 500
            message = "Failed to fetch form data. Please try again."
        if status:
            try:
                new_org_request = self.Requests()
                new_org_request.create_new_request(request.user, company_name)
                new_org_request.save()
                message = "New Organisation Account Access registered. We'll contact you soon."
            except:
                status = False
                code = 500
                message = "Internal Server Error"
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def put(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            request_id = int(arguments.get("id"))
            action = int(arguments.get("action")) # 0 = Accept, 1 = Dismiss
            cancellation_reason = int(arguments.get("reason"))
        except:
            status = False
            code = 500
            message = "Error parsing form data."
        req = None
        if status:
            # Check if this request exist
            access_requests = self.Requests.objects.filter(id = request_id)
            if len(access_requests):
                req = access_requests[0]
            else:
                status = False
                code = 403
                message = "Invalid Organisation Account Access request."
        if status:
            if action is 0:
                try:
                    with transaction.atomic():
                        req.accept_request()
                        req.save()
                        new_org_account = self.OrgAccount()
                        new_org_account.create_new_organisation(req.organisation, [req.organisation], req.user.id)
                        req.user.add_org(new_org_account)
                        req.user.save()
                        message = "Organisation Account Created Successfully"
                except IntegrityError as e:
                    status = False
                    code = 500
                    message = "Organisation name should be unique."
                except:
                    status = False
                    code = 500
                    message = "Internal server error. Contact support."
            elif action is 1:
                try:
                    req.reject_request(cancellation_reason)
                    req.save()
                    message = "Organisation Account Access request cancelled successfully."
                except:
                    status = False
                    code = 500
                    message = "Internal server error. Contact support."
            else:
                status = False
                code = 403
                message = "Invalid action code."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })

    @method_decorator(decorator=[login_required, admin_and_org_admin_only], name='dispatch')
    def delete(self, request, *args, **kwargs):
        """ This function is used by the org admins and admin to delete org account """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            id = int(arguments.get("id"))
        except:
            status = False
            code = 500
            message = "Error parsing data. Contact support."
        org = None
        if status:
            # check if the Org account exist
            orgs = self.OrgAccount.objects.get(id = id)
            if len(orgs):
                org = orgs[0]
            else:
                status = False
                code = 403
                message = "Organisation not found"
        users = None
        if status:
            # Get the user account of org account
            users = User.objects.filter(organisation=org)
            if not len(users):
                status = False
                code = 403
                message = "Organisation Admin not found"
            else:
                try:
                    with transaction.atomic():
                        for u in users:
                            u.user_type = 0
                            u.save()
                        org.delete()
                        message = "Operation Successful. Organisation Account Deleted."
                except:
                    status = False
                    code = 500
                    message = "Internal Server Error. Contact Support."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })
