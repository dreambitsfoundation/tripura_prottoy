from django.db import models
from django.contrib.postgres.fields import ArrayField

from administrator.Models import ArticleCategoryModel
from customer.Models.Post import PostModel
from authentication.models import User
from django.utils import timezone
from utils.ReadableDateTime import generate_readable_date_time
from cloudinary.api import resource, NotFound

class ArticlesModel(models.Model):
    """ This model is used to store the articles written by the admin """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.TextField(default="")
    body = models.TextField(default = "")
    posts = models.ManyToManyField(PostModel)
    photos = ArrayField(models.TextField(default = ""), null=True)
    published = models.BooleanField(default= False)
    draft = models.BooleanField(default=True)
    last_updated = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(default = timezone.now)
    published_on = models.DateTimeField(null=True)
    category = models.ForeignKey(ArticleCategoryModel, on_delete=models.CASCADE, null=True)

    def create_article(self, user:User, title: str, body: str, publish:bool = False, posts:list = None, photos:list = None):
        self.title = title
        self.body = body
        self.user = user
        if posts:
            for p in posts:
                self.posts.add(p)
        if photos:
            self.photos = photos
        self.published = publish
        if self.published:
            self.draft = False
            self.published_on = timezone.now()

    def generate_all_image_urls(self):
        urls = []
        current_photos = self.photos
        final_photos = []
        if self.photos:
            for photo in current_photos:
                try:
                    res = resource(photo)
                    urls.append(res['secure_url'])
                    final_photos.append(photo)
                except NotFound as e:
                    print("not found")
                    pass
                except Exception as e:
                    print(e)
                    final_photos.append(photo)
            self.photos = final_photos
            self.save()
        return urls

    def serialize(self):
        from customer.Models import CommentModel
        comments = []
        all_comments = CommentModel.objects.filter(article=self, head_comment=True)
        for comment in all_comments:
            comments.append(comment.serialize())
        return {
            "id": self.pk,
            "user_id": self.user.pk,
            "user_full_name": self.user.get_full_name(),
            "title": self.title,
            "body": self.body,
            "published_on": generate_readable_date_time(self.published_on) if self.published else "",
            "comments": comments,
            "last_drafted": self.last_updated,
            "created_on": self.created
        }
