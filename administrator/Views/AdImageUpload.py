from django.views import View
from django.views.decorators.csrf import csrf_exempt
from authentication.Decorators.AuthorizationValidator import *
from ..Models import AdImageModel
from django.utils.decorators import method_decorator
from django.db import transaction
import cloudinary

decorators = [csrf_exempt]

@method_decorator(decorator=decorators, name="dispatch")
class AdImageView(View):
    """ This view handles request to ad image related request """
    
    http_method_names = ['get', 'post']

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
                ad_image_instance = self.model.objects.filter(id=0)
                if len(ad_image_instance) == 0:
                    ad_image_instance = self.model()
                    ad_image_instance.save()
                else:
                    ad_image_instance = ad_image_instance[0]
            except:
                raise
                status = False
                code = 500
                message = "Internal Server Error"
        if status:
            if target == "tall":
                try:
                    with transaction.atomic():
                        if len(ad_image_instance.tall_image_id) > 0:
                            ad_image_instance.delete_tall_image()
                            ad_image_instance.save()
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
                        if len(ad_image_instance.wide_image_id) > 0:
                            ad_image_instance.delete_wide_image()
                            ad_image_instance.save()
                        ad_image_instance.update_wide_image(image)
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
