from django.db import models
from django.utils import timezone

from authentication.models import User
from utils.ReadableDateTime import generate_readable_date_time


class PostModel(models.Model):
    """ This model will be used to store the user posts """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.TextField(default="")
    body = models.TextField(default="")
    posted_on = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    organisation = models.TextField(default="")
    organisation_id = models.IntegerField(default=0)
    pending_for_screening = models.BooleanField(default=True)

    def create(self, user: User, title: str, body: str, organisation: str):
        self.user = user
        self.title = title
        self.body = body
        self.organisation = organisation

    def approve(self):
        self.pending_for_screening = False
        self.approved = True

    def reject(self):
        self.pending_for_screening = False
        self.rejected = True

    def serialize(self):
        from customer.Models import CommentModel
        comments = []
        all_comments = CommentModel.objects.filter(post=self, head_comment=True)
        for comment in all_comments:
            comments.append(comment.serialize())
        return {
            "id": self.id,
            "user_id": self.user.pk,
            "user_full_name": self.user.get_full_name(),
            "title": self.title,
            "body": self.body,
            "posted_on": generate_readable_date_time(self.posted_on),
            "comments": comments,
            "approved": self.approved,
            "rejected": self.rejected,
            "pending": self.pending_for_screening,
            "organisation": self.organisation,
            "organisation_id": self.organisation_id
        }
