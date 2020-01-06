from django.db import models
from authentication.models import User
from django.utils import timezone
import pytz
from django.conf.global_settings import TIME_ZONE

class OrgAccessRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organisation = models.TextField(null=True)
    pending = models.BooleanField(default=True)
    accepted = models.BooleanField(default = False)
    cause_of_rejection = models.TextField(default = "")
    requested_on = models.DateTimeField(default=timezone.now)
    process_completed_on = models.DateTimeField(null=True)


    def create_new_request(self, user:User, organisation: str):
        self.user = user
        self.organisation = organisation

    def accept_request(self):
        self.pending = False
        self.accepted = True
        self.process_completed_on = timezone.now()

    def reject_request(self, reason:str):
        self.cause_of_rejection = reason
        self.pending = False
        self.accepted = False
        self.process_completed_on = timezone.now()

    def serialize(self):
        tz = pytz.timezone(TIME_ZONE)
        return {
            "id": self.id,
            "user": self.user.serialize() if self.user else {},
            "organisation": self.organisation if self.organisation else "",
            "pending": self.pending,
            "accepted": self.accepted,
            "request_date": self.requested_on,
            "complete_date": self.process_completed_on.astimezone(tz=tz).strftime('%a, %d %B %Y %I:%M:%S %p') if self.process_completed_on else ""
        }
