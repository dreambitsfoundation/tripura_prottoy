from django.db import models
from administrator.Models.StaticArticle import StaticArticleModel


class StaticCategoryModel(models.Model):
    """ This model holds all the categories used to mention on the homepage category """
    name = models.TextField(null=True)
    sub_categories = models.ManyToManyField("self")
    articles = models.ManyToManyField(StaticArticleModel)
    head_category = models.BooleanField(default=True)
    
    def serialize(self):
        cat = {
            "name": self.name,
            "head_category": self.head_category,
            "id": self.id
        }
        if not self.head_category:
            sub_category = []
            for sub in self.sub_categories:
                sub_cat = {
                    "name": sub.name,
                    "id": sub.id,
                    "head_category": False
                }
                sub_category.append(sub_cat)
            cat["sub_categories"] = sub_category
        return cat
