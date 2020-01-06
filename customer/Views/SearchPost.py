from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from authentication.Decorators.AuthorizationValidator import login_required, admin_only
from customer.Models import PostModel
from authentication.models import User
from utils.JsonRequestParserMiddleware import JsonRequestParser
from functools import reduce
import operator


@method_decorator(csrf_exempt, name='dispatch')
class SearchPostView(View):

    model = PostModel
    user = User

    @method_decorator(decorator=login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        try:
            query = request.GET['q']
            split_query = query.split(" ")
            # tag_qs = reduce(operator.and_, (Q(body__contains=x) for x in split_query))
            # print(tag_qs)
            posts = self.model.objects.filter(Q(title__contains=query)|Q(body__contains=query)).distinct()
        except:
            status = False
            code = 500
            message = "Error parsing data."
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": [post.serialize() for post in posts]
        }
        return JsonResponse(resp, status=code)