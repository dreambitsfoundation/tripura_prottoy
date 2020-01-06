from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from administrator.Models import StaticCategoryModel
from authentication.Decorators.AuthorizationValidator import *
from utils.JsonRequestParserMiddleware import JsonRequestParser


@method_decorator(decorator=[csrf_exempt], name='dispatch')
class AddStaticCategoryView(View):
    """ This view holds all operations related to adding static category """

    http_method_names = ['get', 'post', 'put', 'delete']

    Category = StaticCategoryModel

    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def get(self, request, *args, **kwargs):
        """ Returns all the static categories and sub categories """
        status = True
        code = 200
        message = ""
        data = []
        try:
            categories = self.Category.objects.filter(head_category = True)
            data = [c.serialize() for c in categories]
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
        """ Returns all the categories and sub categories """
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
            # Check for existing categories
            categories = self.Category.objects.filter(name = name)
            if len(categories):
                status = False
                code = 403
                message= "Category already exist."
        parent_category = None
        if status:
            # Check if the parent id is proper then fetch the parent category
            if parent_id is not 0:
                parents = self.Category.objects.filter(id = parent_id)
                if len(parents):
                    parent_category = parents[0]
                else:
                    status = False
                    code = 403
                    message = "Invalid parent category."
        if status:
            # Create a new category
            try:
                with transaction.atomic():
                    category = self.Category()
                    category.name = name
                    category.save()
                    if parent_category is not None:
                        category.head_category = False
                        category.save()
                        parent_category.sub_categories.add(category)
                        parent_category.save()
                    message = "Category added successfully"
            except:
                raise
                status = False
                code = 500
                message = "Internal server error."
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message
        })
    
    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def put(self, request, *args, **kwargs):
        """ Used to update the existing category items """
        status = True
        code = 200
        message = ""
        data = []
        arguments = JsonRequestParser(request)
        try:
            name = arguments.get("name")
            id = int(arguments.get("id"))
        except:
            status = False
            code = 500
            message = "Error parsing form data."
        if status:
            # Check if the category exists
            categories = self.Category.objects.filter(id=id)
            if len(categories):
                category = categories[0]
            else:
                status = False
                code = 403
                message = "Category not found"
        if status:
            # Check if another category with the same name does exist
            categories = self.Category.objects.filter(name = name)
            if len(categories):
                temp = categories[0]
                if temp.id != category.id:
                    status = False
                    code = 403
                    message = "Category with the same name already exists."
        if status:
            # Update the existing record
            try:
                category.name = name
                category.save()
                message = "Record successfully updated"
            except:
                status = False
                code = 500
                message = "Internal Server Error"
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message
        })
    
    @method_decorator(decorator=[login_required, admin_only], name='dispatch')
    def delete(self, request, *args, **kwargs):
        """ Used to delete the existing category items """
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
        if status:
            # Check if the category exists
            categories = self.Category.objects.filter(id=id)
            if len(categories):
                category = categories[0]
            else:
                status = False
                code = 403
                message = "Category not found"
        if status:
            # Delete the existing record
            try:
                category.delete()
                message = "Record successfully deleted"
            except:
                status = False
                code = 500
                message = "Internal Server Error"
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message
        })