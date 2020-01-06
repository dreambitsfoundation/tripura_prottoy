from django.db import models


class StaticArticleModel(models.Model):
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    category_id = models.IntegerField(default=0)
