from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from authentication.Decorators.AuthorizationValidator import login_required, admin_only
from customer.Models import PostModel
from administrator.Models import ArticlesModel
from authentication.models import User
from utils.JsonRequestParserMiddleware import JsonRequestParser
from cloudinary.uploader import upload
from cloudinary.api import resource, delete_resources, NotFound
from cloudinary import CloudinaryImage


@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(View):

    @method_decorator(decorator=login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        try:
            public_id = request.GET['public_id']
        except:
            status = False
            code = 500
            message = "Error parsing request data"
        if status:
            try:
                res = resource(public_id)
                data = [res['secure_url']]
                # Above approach is ok but the following is more simple
                #url = CloudinaryImage(public_id).image(secure=True)
                # This will return result with image tag
                # '<img src="https://res.cloudinary.com/indianconsumers-org/image/upload/sample.jpg"/>'
            except NotFound as e:
                status = False
                code = 404
                message = "Resource Not Found on CDN"
            except:
                status = False
                code = 500
                message = "CDN communication failed"
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": []
        }
        return JsonResponse(resp, status=code)

    @method_decorator(decorator=login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        print("request is here")
        print(request.FILES)
        try:
            image = request.FILES['image']
        except:
            raise
            status = False
            code = 500
            message = "Error parsing request data"
        if status:
            try:
                result = upload(image)
                data = [{"public_id": result['public_id'], "secure_urls": result['secure_url']}]
            except:
                raise
                status = False
                code = 500
                message = "Internal server error"
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }
        return JsonResponse(resp)

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def delete(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            public_id = arguments.get("public_id")
        except:
            status = False
            code = 500
            message = "Error parsing request data"
        if status:
            try:
                result = delete_resources([public_id])
            except:
                status = False
                code = 500
                message = "Internal server error"
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }
        return JsonResponse(resp, status=code)
