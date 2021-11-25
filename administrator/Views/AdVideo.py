from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from administrator.models import AdVideoModel
decorators = [csrf_exempt]


@method_decorator(csrf_exempt, name='dispatch')
class AdVideoView(View):
    http_method_names=['get', 'post', 'delete']

    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = {}

        videos = AdVideoModel.objects.all()

        data = [{"id": video.id, "link": video.link} for video in videos]

        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": data
        })

    def post(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = {}

        try:
            url = request.POST.get("url")
        except:
            status = False
            code = 500
            message = "Error parsing form data"
        if status:
            video = AdVideoModel(link=url)
            video.save()
        
        return JsonResponse({
            "status": status,
            "code": code,
            "message": message,
            "data": []
        })

    def delete(self, request, *args, **kwargs):
        print("This function was triggered")
        status = True
        code = 200
        message = ""
        data = {}

        try:
            id = request.GET["id"]
            print(id)
        except:
            raise
            status = False
            code = 500
            message = "Error parsing request data"

        if status:
            videos = AdVideoModel.objects.filter(id=id)
            if len(videos):
                video = videos[0]
            else:
                status = False
                code = 403
                message = "Video not found"
        if status:
            try:
                video.delete()
                message = "Video is successfully deleted"
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
