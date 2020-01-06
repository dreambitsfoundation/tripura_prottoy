from functools import wraps

from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout

from authentication.models import SuperAdminSetup
from utils.JWTManager import JWTManager

""" Permission Related Authorisation Decorators """


def require_admin_dashboard_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_admin_dashboard_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_geo_location_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_geo_location_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_google_places_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_google_places_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_geo_tracking_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_geo_tracking_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_partner_app_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_partner_app_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_customer_app_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_customer_app_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_image_upload_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_image_upload_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_geo_fencing_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_geo_fencing_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_services_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_services_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_customer_signup_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_customer_signup_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


def require_partner_signup_enabled_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        master_settings = SuperAdminSetup.objects.all()
        if len(master_settings) and master_settings[0].is_partner_signup_enabled():
            return function(request, *args, **kwargs)
        return JsonResponse({"status": False, "message": "FEATURE NOT ALLOWED", "code": 403}, status=403)
    return decorator


""" Authentication Related Authorisation Decorators """


def login_required(function):
    @wraps(function)
    def decorator(request,*args,**kwargs):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token is None:
            # Check the cookie once
            auth_token = request.COOKIES.get('HTTP_AUTHORIZATION')
        if auth_token is not None:
            auth_token = auth_token.split(" ")[-1]
            token_manager = JWTManager()
            token_valid = token_manager.validate_token(auth_token)
            # check if the token is a refresh token
            is_ref_token = token_manager.is_refresh_token()
            if is_ref_token:
                return JsonResponse({"status": False, "message": "INVALID AUTHORIZATION", "code": 401}, status=401)
            user = None
            if token_valid:
                user = token_manager.get_user()
            else:
                return JsonResponse({"status": False, "message": "SESSION EXPIRED", "code": 401}, status=401)
            if user is not None:
                request.user = user
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False, "message": "UNAUTHORIZED", "code": 401}, status=401)
        else:
            return JsonResponse({"status": False, "message": "AUTHORIZATION NOT AVAILABLE", "code": 401}, status=401)
    return decorator


def allow_http_cookie_authorization(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        try:
            auth_token = request.COOKIES['HTTP_AUTHORIZATION']
            if auth_token is not None:
                request.META['HTTP_AUTHORIZATION'] = auth_token
                return function(request, *args, *kwargs)
        except Exception as e:
            pass
    return decorator


def unauthorized_user_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token is not None:
            return JsonResponse({"status": False, "message": "AUTHORIZED USERS NOT ALLOWED", "code": 405}, status=405)
        else:
            return function(request, *args, **kwargs)
    return decorator


def super_admin_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user is not None:
            if request.user.user_type is 3:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
        else:
            return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
    return decorator


def admin_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user is not None:
            if request.user.user_type is 2:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
        else:
            return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
    return decorator


def admin_and_org_admin_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user is not None:
            if request.user.user_type is [2, 4]:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
        else:
            return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
    return decorator


def standard_user_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user is not None:
            if request.user.user_type is 0:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
        else:
            return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
    return decorator


def service_provider_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user is not None:
            if request.user.user_type is 1:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
        else:
            return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
    return decorator


def non_admin_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user is not None:
            if request.user.user_type in [0, 1, 4]:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
        else:
            return JsonResponse({"status": False, "message": "INVALID ACCESS AUTHORIZATION", "code": 401}, status=401)
    return decorator


""" Route Validator """


def admin_only_route(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.user is not None:
            if request.user.user_type is 2:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("")
        else:
            return HttpResponseRedirect("")
    return decorator


def parse_user_profile(function):
    @wraps(function)
    def decorator(request,*args,**kwargs):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token is None:
            # Check the cookie once
            auth_token = request.COOKIES.get('HTTP_AUTHORIZATION')
        if auth_token is not None:
            auth_token = auth_token.split(" ")[-1]
            token_manager = JWTManager()
            token_valid = token_manager.validate_token(auth_token)
            # check if the token is a refresh token
            is_ref_token = token_manager.is_refresh_token()
            user = None
            if token_valid:
                user = token_manager.get_user()
            if user is not None:
                request.user = user
            else:
                request.user = None
        return function(request, *args, **kwargs)
    return decorator
