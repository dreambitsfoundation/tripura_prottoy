from django.db import models
from django.utils import timezone


class ArticleCategoryModel(models.Model):
    name = models.TextField(null=False, unique=True)
    created = models.DateTimeField(default=timezone.now)
    parent_category = models.BooleanField(default=True)
    sub_categories = models.ManyToManyField("self")

    def create_new(self, name:str):
        self.name = name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent": self.parent_category,
            "sub_category": [cat.serialize() for cat in self.sub_categories.all()] if self.parent_category else []
        }