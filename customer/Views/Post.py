from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from authentication.Decorators.AuthorizationValidator import login_required, admin_only
from customer.Models import PostModel
from authentication.models import User
from utils.JsonRequestParserMiddleware import JsonRequestParser


@method_decorator(csrf_exempt, name='dispatch')
class MakePostView(View):

    model = PostModel
    user = User

    @method_decorator(decorator=login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        try:
            post_id = request.GET['post_id']
            posts = self.model.objects.filter(id=int(post_id))
        except:
            posts = self.model.objects.filter(user=request.user).order_by("-posted_on")
        print(posts)
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": [post.serialize() for post in posts]
        }
        return JsonResponse(resp, status=code)

    @method_decorator(decorator=login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            heading = arguments.get("head")
            body = arguments.get("body")
            organisation = arguments.get("organisation")
        except:
            status = False
            code = 500
            message = "Error parsing request data"
        if status:
            try:
                post = self.model()
                post.create(request.user, heading, body, organisation)
                post.save()
                message = "Post is successfully created and is pending for approval."
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

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def put(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            id = int(arguments.get("id"))
            publish = arguments.get("publish")
        except:
            status = False
            code = 500
            message = "Error parsing request data"
        if status:
            if isinstance(publish, str):
                if publish == 'True':
                    publish = True
                if publish == 'False':
                    publish = False
        post = None
        if status:
            posts = self.model.objects.filter(id=id)
            if len(posts):
                post = posts[0]
            else:
                status = False
                code = 403
                message = "Post not found"
        if status:
            try:
                if publish:
                    post.approve()
                    post.save()
                else:
                    post.reject()
                    post.save()
                message = "Post status is successfully updated"
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

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def delete(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            id = arguments.get("id")
        except:
            status = False
            code = 500
            message = "Error parsing request data"
        post = None
        if status:
            posts = self.model.objects.filter(id=id)
            if len(posts):
                post = posts[0]
            else:
                status = False
                code = 403
                message = "Post not found"
        if status:
            try:
                post.delete()
                message = "Post is successfully deleted"
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
