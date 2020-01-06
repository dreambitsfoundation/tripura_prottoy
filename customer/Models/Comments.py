from django.db import models
from django.utils import timezone

from customer.Models.Post import PostModel
from administrator.Models.Articles import ArticlesModel
from authentication.models import User
from utils.ReadableDateTime import generate_readable_date_time


class CommentModel(models.Model):
    """ This model will be used store comments with respect to Posts """
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(ArticlesModel, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    head_comment = models.BooleanField(default=False)
    sub_comment = models.ManyToManyField("self")
    last_updated = models.DateTimeField(default=timezone.now)

    def add_post_comment(self, post: PostModel, user: User, text: str, head_comment: bool):
        self.post = post
        self.user = user
        self.text = text
        self.head_comment = head_comment
    
    def add_article_comment(self, article: ArticlesModel, user: User, text: str, head_comment: bool):
        self.article = article
        self.user = user
        self.text = text
        self.head_comment = head_comment

    def serialize(self, loop = 0):
        sub_comments = []
        if loop < 2:
            for comment in self.sub_comment.all():
                sub_comments.append(comment.serialize(loop+1))
        return {
            "id": self.pk,
            "post_id": self.post.pk,
            "user_id": self.user.pk,
            "user_full_name": self.user.get_full_name(),
            "last_updated": generate_readable_date_time(self.last_updated),
            "sub_comments": sub_comments,
            "text": self.text,
            "head_comment": self.head_comment
        }