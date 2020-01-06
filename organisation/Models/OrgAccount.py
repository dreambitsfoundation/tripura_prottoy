from django.db import models
import pytz
from django.conf.global_settings import TIME_ZONE
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class OrgAccountModel(models.Model):
    """ Model containing configuration about the company profile """
    name = models.TextField(null=True, unique=True)
    tags = ArrayField(models.TextField(null=True))
    admin_user_id = models.IntegerField(null=True)
    created = models.DateTimeField(default = timezone.now)
    last_updated = models.DateTimeField(null=True)

    def create_new_organisation(self, name: str, tags: list, admin_user_id: int):
        self.name = name
        self.tags = tags
        self.admin_user_id = admin_user_id
        self.last_updated = timezone.now()
        self.save()
    
    def change_admin_user(self, admin_user_id: int):
        self.admin_user_id = admin_user_id
        self.last_updated = timezone.now()
        self.save()
    
    def change_tags(self, tags: list):
        self.tags = tags
        self.last_updated = timezone.now()
        self.save()
