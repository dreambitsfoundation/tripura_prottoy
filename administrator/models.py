from django.db import models


class AdVideoModel(models.Model):
    """
    This model store all the ad videos.
    """

    link = models.TextField(null=False)
    created = models.DateField(auto_now=True)
