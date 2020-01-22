from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

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
    photos = ArrayField(JSONField(default=""), null=True)
    videos = ArrayField(models.TextField(default=""), null=True)
    published = models.BooleanField(default= False)
    draft = models.BooleanField(default=True)
    last_updated = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(default = timezone.now)
    published_on = models.DateTimeField(null=True)
    category = models.ForeignKey(ArticleCategoryModel, on_delete=models.CASCADE, null=True)
    views = models.IntegerField(default=0)

    def create_article(self, user:User, title: str, body: str, publish:bool = False, posts:list = None, photos:list = None, videos:list = None):
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
        if videos:
            self.videos = videos

    def generate_all_image_urls(self):
        urls = []
        card_urls = []
        current_photos = self.photos
        final_photos = []
        if self.photos:
            for photo in current_photos:
                try:
                    urls.append(photo['secure_urls'])
                    current_url = photo['secure_urls']
                    current_url = current_url.split("/")
                    card_urls.append(self.crop_to_card_size(current_url))
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

    def generate_card_image_urls(self):
        card_urls = []
        current_photos = self.photos
        final_photos = []
        if self.photos:
            for photo in current_photos:
                try:
                    current_url = photo['secure_urls']
                    current_url = current_url.split("/")
                    card_urls.append(self.crop_to_card_size(current_url))
                    final_photos.append(photo)
                except NotFound as e:
                    print("not found")
                    pass
                except Exception as e:
                    print(e)
                    final_photos.append(photo)
            self.photos = final_photos
            self.save()
        return card_urls

    def generate_thumbnail_image_urls(self):
        card_urls = []
        current_photos = self.photos
        final_photos = []
        if self.photos:
            for photo in current_photos:
                try:
                    current_url = photo['secure_urls']
                    current_url = current_url.split("/")
                    card_urls.append(self.crop_to_thumbnail_size(current_url))
                    final_photos.append(photo)
                except NotFound as e:
                    print("not found")
                    pass
                except Exception as e:
                    print(e)
                    final_photos.append(photo)
            self.photos = final_photos
            self.save()
        return card_urls

    def crop_to_card_size(self, url:list):
        final = ""
        if len(url) == 8:
            url[-2] = "w_300,h_200,c_fill"            
        elif len(url) == 7:
            url.insert(6, "w_300,h_200,c_fill")
        for index, piece in enumerate(url):
            final = final + piece
            if index < len(url)-1:
                final = final + "/"
        return final

    def crop_to_thumbnail_size(self, url:list):
        final = ""
        if len(url) == 8:
            url[-2] = "h_200,c_fill"            
        elif len(url) == 7:
            url.insert(6, "h_200,c_fill")
        for index, piece in enumerate(url):
            final = final + piece
            if index < len(url)-1:
                final = final + "/"
        return final

    def add_one_view(self):
        self.views = self.views + 1

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
            "created_on": self.created,
            "total_views": self.views
        }
