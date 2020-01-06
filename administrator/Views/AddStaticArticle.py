from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..Models import StaticArticleModel, StaticCategoryModel
from authentication.Decorators.AuthorizationValidator import *
from utils.JsonRequestParserMiddleware import JsonRequestParser


@method_decorator(decorator=[csrf_exempt], name='dispatch')
class AddStaticArticleView(View):
    """ This view holds all operations related to adding static category """

    http_method_names = ['get', 'post']

    Category = StaticCategoryModel
    model = StaticArticleModel

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def get(self, request, *args, **kwargs):
        """" Returns all the static articles """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            article_id = arguments.get_or_none("category_id")
        except:
            status = False
        # TODO: Complete this function
        

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def post(self, request, *args, **kwargs):
        """" Use this function to add static article """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            title = arguments.get("title")
            body = arguments.get("body")
            category_id = int(arguments.get("category_id"))
        except:
            status = False
            code = 500
            message = "Error parsing form data."
        category = None
        if status:
            # Check for existing categories
            categories = self.Category.objects.filter(id = category_id)
            if len(categories):
                category = categories[0]
            else:
                status = False
                code = 403
                message = "Category does not exist."
        if status:
            # Check any article with the same name already exist in this category
            articles = category.articles.all()
            for a in articles:
                if a.title == title:
                    status = False
                    code = 403
                    message = "Article with the same name already exist in this category"
                    break
        if status:
            # Create a new article and add it to the category
            try:
                with transaction.atomic():
                    article = self.model(title=title, content=body, category_id=category_id)
                    article.save()
                    category.articles.add(article)
                    category.save()
                    message = "Article added successfully"
            except:
                status = False
                code = 500
                message = "Internal server error."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message
        })
