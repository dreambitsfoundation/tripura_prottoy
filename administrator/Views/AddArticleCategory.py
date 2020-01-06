from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from administrator.Models import ArticleCategoryModel
from authentication.Decorators.AuthorizationValidator import admin_only, login_required
from utils.JsonRequestParserMiddleware import JsonRequestParser
from django.db import transaction


@method_decorator(decorator=[csrf_exempt], name='dispatch')
class AddArticleCategoryView(View):
    """ This view is used to create and update Article Categories """

    http_method_names = ['get', 'post', 'put', 'delete']

    # Models
    model = ArticleCategoryModel

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        try:
            all_categories = self.model.objects.all()
            data = [c.serialize() for c in all_categories]
        except:
            status = False
            code = 500
            message = "Internal Server Error."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def post(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            name = arguments.get("name")
            parent_id = int(arguments.get("parent_id"))
        except:
            status = False
            code = 500
            message = "Error parsing form data."
        if status:
            parent = None
            if parent_id is not 0:
                parents = self.model.objects.filter(id = parent_id)
                if len(parents) > 0:
                    parent = parents[0]
                else:
                    status = False
                    code = 403
                    message = "Parent Category Not Found."
        if status:
            try:
                with transaction.atomic():
                    record = self.model()
                    record.create_new(name)
                    record.save()
                    if parent is not None:
                        record.parent_category = False
                        record.save()
                        parent.sub_categories.add(record)
                        parent.save()
            except IntegrityError as e:
                status = False
                code = 403
                message = "Category already exist."
            except:
                status = False
                code = 500
                message = "Internal Server Error."
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
            id = int(arguments.get("id"))
            name = arguments.get("name")
        except:
            status = False
            code = 500
            message = "Error parsing form data."
        record = None
        if status:
            records = self.model.objects.filter(id=id)
            if len(records):
                record = records[0]
            else:
                status = False
                code = 403
                message = "Category name not available."
        if status:
            try:
                record.name = name
                record.save()
            except IntegrityError as e:
                status = False
                code = 403
                message = "Category name already exist."
            except:
                status = False
                code = 500
                message = "Internal Server Error."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def delete(self, request, *args, **kwargs):
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
            message = "Error parsing form data."
        record = None
        if status:
            records = self.model.objects.filter(id=id)
            if len(records):
                record = records[0]
            else:
                status = False
                code = 403
                message = "Category name not available."
        if status:
            try:
                record.delete()
            except IntegrityError as e:
                status = False
                code = 403
                message = "Category name already exist."
            except:
                status = False
                code = 500
                message = "Internal Server Error."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })
