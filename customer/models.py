from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from django.utils import timezone


class NewsLetterSession(models.Model):
    init_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    posts = ArrayField(models.IntegerField(default=0))
    articles = ArrayField(models.IntegerField(default=0))

    def create_new_session(self, posts, articles):
        pass

