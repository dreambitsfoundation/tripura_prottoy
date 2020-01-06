from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from authentication.Decorators.AuthorizationValidator import login_required, admin_only
from customer.Models import PostModel
from administrator.Models import ArticlesModel, ArticleCategoryModel
from authentication.models import User
from utils.JsonRequestParserMiddleware import JsonRequestParser
from django.db import transaction


@method_decorator(csrf_exempt, name='dispatch')
class ArticleView(View):

    model = ArticlesModel
    posts = PostModel
    category = ArticleCategoryModel
    user = User

    #@method_decorator(decorator=login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        try:
            article_id = request.GET['article_id']
            print(article_id)
            articles = self.model.objects.filter(id=int(article_id))
        except:
            articles = self.model.objects.filter(user=request.user).order_by("-published_on")
        print(articles)
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": [article.serialize() for article in articles]
        }
        return JsonResponse(resp, status=code)

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def post(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            heading = arguments.get("head")
            body = arguments.get("body")
            images = arguments.get("images")
            posts = arguments.get("posts")   
            publish = bool(arguments.get("publish"))
            draft = bool(arguments.get("draft"))
            category_id = int(arguments.get("category_id"))
        except:
            raise
            status = False
            code = 500
            message = "Error parsing request data"
        category = None
        if status:
            categories = self.category.objects.filter(id = category_id)
            if len(categories):
                category = categories[0]
            else:
                status = False
                code = 403
                message = "Category not found"
        if status:
            try:
                with transaction.atomic():
                    article = self.model()
                    article.save()
                    article.create_article(
                        user = request.user,
                        title=heading,
                        body=body,
                        photos= images,
                        posts= posts,
                        publish=publish
                    )
                    article.category = category
                    article.save()
                    print(article.id)
                    message = "Article is successfully created."
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
