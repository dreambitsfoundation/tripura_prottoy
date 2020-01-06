from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from authentication.Decorators.AuthorizationValidator import login_required
from customer.Models.Comments import CommentModel
from customer.Models.Post import PostModel
from administrator.Models import ArticlesModel
from utils.JsonRequestParserMiddleware import JsonRequestParser


@method_decorator(csrf_exempt, name='dispatch')
class PostCommentView(View):

    model = CommentModel
    posts = PostModel
    articles = ArticlesModel

    @method_decorator(decorator=login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        status = True
        code = 200
        message = ""
        data = []
        comments = self.model.objects.filter(user=request.user).order_by("-last_updated")
        resp = {
            "status": status,
            "code": code,
            "message": message,
            "data": [comment.serialize(1) for comment in comments]
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
            text = arguments.get("text")
            head_comment = arguments.get("head_comment")  # This is a boolean value
            post_id = arguments.get_or_none("post_id")
            article_id = arguments.get_or_none("article_id")
            root_comment_id = int(arguments.get("root_comment_id"))  # Shall be only considered if head_comment is false
        except:
            raise
            status = False
            code = 500
            message = "Error parsing request data"
        if status:
            if post_id:
                post_id = int(post_id)
            if article_id:
                article_id = int(article_id)
            if isinstance(head_comment, (str)):
                if head_comment == "True":
                    head_comment = True
                if head_comment == "False":
                    head_comment = False
        post = None
        if status:
            if post_id:
                posts = self.posts.objects.filter(id = post_id)
                if len(posts):
                    post = posts[0]
                else:
                    status = False
                    code = 403
                    message = "Post not found"
            if article_id:
                articles = self.articles.objects.filter(id = article_id)
                if len(articles):
                    article = articles[0]
                else:
                    status = False
                    code = 403
                    message = "Article not found"
        root_comment = None
        if status:
            if not head_comment:
                if post_id:
                    comments = self.model.objects.filter(post=post, id=root_comment_id)
                if article_id:
                    comments = self.model.objects.filter(article=article, id=root_comment_id)
                if len(comments):
                    root_comment = comments[0]
                else:
                    status = False
                    code = 403
                    message = "Root comment not found"
        if status:
            try:
                with transaction.atomic():
                    comment = self.model()
                    if post_id:
                        comment.add_post_comment(
                            post=post,
                            user=request.user,
                            text=text,
                            head_comment=head_comment
                        )
                    if article_id:
                        comment.add_article_comment(
                            article=article,
                            user=request.user,
                            text=text,
                            head_comment=head_comment
                        )
                    comment.save()
                    if not head_comment:
                        root_comment.sub_comment.add(comment)
                        root_comment.save()
                message = "Comment is successfully posted"
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