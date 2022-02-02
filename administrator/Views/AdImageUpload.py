from django.db.models import Q
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from authentication.Decorators.AuthorizationValidator import *
from utils.JsonRequestParserMiddleware import JsonRequestParser
from ..Models import AdImageModel
from django.utils.decorators import method_decorator
from django.db import transaction
import cloudinary

decorators = [csrf_exempt]

@method_decorator(decorator=decorators, name="dispatch")
class AdImageView(View):
    """ This view handles request to ad image related request """
    
    http_method_names = ['get', 'post', 'delete']

    model = AdImageModel

    def get(self, request, *args, **kwargs):
        """ Returns the serialized version of the stored ad image urls """
        status = True
        code = 200
        message = ""
        data = []
        try:
            ad_image_instance = self.model.objects.filter(id=1)
            if len(ad_image_instance) == 0:
                ad_image_instance = self.model()
                ad_image_instance.save()
            else:
                ad_image_instance = ad_image_instance[0]
        except:
            status = False
            code = 500
            message = "Internal Server Error"
        if status:
            data = [ad_image_instance.serialize()]
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })
    
    @method_decorator(decorator=[admin_only], name="dispatch")
    def post(self, request, *args, **kwargs):
        """ Stores Ad Images In server """
        status = True
        code = 200
        message = ""
        data = []
        print(request.FILES)
        try:
            image = request.FILES['image']
            print(request.POST.get("purpose"))
        except:
            raise
            status = False
            code = 500
            message = "Error parsing request data"
        if status:
            target = request.POST.get("purpose", None)
            if target is None:
                status = False
                code = 403
                message = "Purpose not provided"
        if status:
            try:
                """
                THIS WAS THE INITIAL LOGIC FOR SINGLE AD. BASED SYSTEM
                ------------------------------------------------------

                ad_image_instance = self.model.objects.all().first()
                print(ad_image_instance)
                if not ad_image_instance:
                    ad_image_instance = self.model()
                    ad_image_instance.save()
                """
                ad_image_instance = self.model()
                ad_image_instance.save()
            except:
                raise
                status = False
                code = 500
                message = "Internal Server Error"
        if status:
            if target == "tall":
                try:
                    with transaction.atomic():
                        ad_image_instance.update_tall_image(image)
                        ad_image_instance.save()
                except:
                    raise
                    status = False
                    code = 500
                    message = "Internal Server Error"
            if target == "wide":
                try:
                    with transaction.atomic():
                        ad_image_instance.update_wide_image(image)
                        print(ad_image_instance.wide_image_secure_url)
                        ad_image_instance.save()
                except:
                    raise
                    status = False
                    code = 500
                    message = "Internal Server Error"
            if target == "tender":
                try:
                    with transaction.atomic():
                        ad_image_instance.update_tender_image(image)
                        print(ad_image_instance.tender_image_secure_url)
                        ad_image_instance.save()
                except:
                    raise
                    status = False
                    code = 500
                    message = "Internal Server Error"
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })

    @method_decorator(decorator=[admin_only], name="dispatch")
    def delete(self, request, *args, **kwargs):
        """ Used to delete the existing category items """
        status = True
        code = 200
        message = ""
        data = []
        try:
            image_id = request.GET['id']
        except:
            status = False
            code = 500
            message = "Error parsing form data."
        if status:
            # Check if the category exists
            ad_images = AdImageModel.objects.filter(
                Q(wide_image_id=image_id) | Q(tall_image_id=image_id) | Q(tender_image_id=image_id))
            if not ad_images.count():
                status = False
                code = 403
                message = "Ad image not found"
        if status:
            # Delete the existing record
            try:
                ad_images.delete()
                message = "Ad Image successfully deleted"
            except:
                status = False
                code = 500
                message = "Internal Server Error"
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message
        })
