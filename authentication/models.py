import pytz
from django.conf.global_settings import TIME_ZONE
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

# Create your models here.
from django.utils import timezone
from organisation.Models import OrgAccountModel
from utils.UniqueCodeGenerator import generate_key


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    """ This is the custom User models """
    user_id = models.TextField(null=False)
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    email = models.EmailField(null=False, unique=True)
    phone_number = models.TextField(max_length=10, null=False)
    user_type = models.IntegerField(default=0)
    # user_type: 0 = Standard User, 1 = ServicePartner, 2 = Administrator 3 = SuperAdmin 4 = OrgAdmin
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    user_profile_image_record = models.IntegerField(null=True)
    user_profile_image_url = models.TextField(default="")
    state = models.TextField(default="")
    city = models.TextField(default="")
    organisation = models.ForeignKey(OrgAccountModel, on_delete=models.SET_NULL, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    # Used when creating a new account
    def create_new(self, first_name: str, last_name: str, phone_number: str, password: str, state: str, city: str,
                   email: str):
        self.user_id = generate_key(first_name + last_name + email + phone_number + password, 8)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.state = state
        self.city = city
        self.set_password(password)

    # Used when updating user account
    def update(self, first_name: str, last_name: str, phone_number: str, email: str, state: str, city: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.last_updated = timezone.now()
        self.city = city
        self.state = state

    def add_org(self, organisation: OrgAccountModel):
        self.user_type = 4
        self.organisation = organisation

    # Used to set the index of the ImageBucket instance for user's profile image
    def set_user_profile_image(self, index: int):
        self.user_profile_image_record = index

    # Used to change the password
    def change_password(self, password):
        self.set_password(password)
        self.last_updated = timezone.now()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.get_full_name()

    # Utility functions
    def is_standard_user(self):
        return True if self.user_type is 0 else False

    def is_service_provider(self):
        return True if self.user_type is 1 else False

    def is_administrator(self):
        return True if self.user_type is 2 else False

    def is_super_admin(self):
        return True if self.user_type is 3 else False

    def get_user_type(self):
        if self.user_type is 0:
            return "Standard User Account"
        if self.user_type is 1:
            return "Service Partner"
        if self.user_type is 2:
            return "Administrator Account"

    def serialize(self):
        tz = pytz.timezone(TIME_ZONE)
        return {
            "user_id": self.user_id,
            "first_name": self.get_short_name(),
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "email": self.email,
            "phone": self.phone_number,
            "type": self.get_user_type(),
            "profile_image_url": self.user_profile_image_url,
            "created": self.created.astimezone(tz=tz).strftime('%a, %d %B %Y %I:%M:%S %p'),
            "last_updated": self.last_updated.astimezone(tz=tz).strftime('%a, %d %B %Y %I:%M:%S %p'),
            "id": self.id
        }


class SuperAdminSetup(models.Model):
    """ This class contains all feature access allowed to the business """
    geo_location_enabled = models.BooleanField(default=False)
    google_places_enabled = models.BooleanField(default=False)
    geo_tracking_enabled = models.BooleanField(default=False)
    partner_app_enabled = models.BooleanField(default=False)
    customer_app_enabled = models.BooleanField(default=False)
    admin_dashboard_enabled = models.BooleanField(default=False)
    image_upload_enabled = models.BooleanField(default=False)
    geo_fencing_enabled = models.BooleanField(default=False)
    services_enabled = models.BooleanField(default=False)
    customer_signup_enabled = models.BooleanField(default=False)
    partner_signup_enabled = models.BooleanField(default=False)

    def is_geo_location_enabled(self):
        return self.geo_location_enabled

    def is_google_places_enabled(self):
        return self.google_places_enabled

    def is_geo_tracking_enabled(self):
        return self.geo_tracking_enabled

    def is_partner_app_enabled(self):
        return self.partner_app_enabled

    def is_customer_app_enabled(self):
        return self.customer_app_enabled

    def is_admin_dashboard_enabled(self):
        return self.admin_dashboard_enabled

    def is_image_upload_enabled(self):
        return self.image_upload_enabled

    def is_geo_fencing_enabled(self):
        return self.geo_fencing_enabled

    def is_services_enabled(self):
        return self.services_enabled

    def is_customer_signup_enabled(self):
        return self.customer_signup_enabled

    def is_partner_signup_enabled(self):
        return self.customer_signup_enabled

    def init_basic_access_permission(self):
        self.admin_dashboard_enabled = True
        self.customer_signup_enabled = True
        self.image_upload_enabled = True
        self.services_enabled = True

    def update_permission(self, geo_location, google_places, geo_traking, partner_app, customer_app, admin_dashboard,
                          image_upload, geo_fencing, services, customer_signup, partner_signup):
        self.geo_location_enabled = geo_location
        self.google_places_enabled = google_places
        self.geo_tracking_enabled = geo_traking
        self.partner_app_enabled = partner_app
        self.customer_app_enabled = customer_app
        self.admin_dashboard_enabled = admin_dashboard
        self.image_upload_enabled = image_upload
        self.geo_fencing_enabled = geo_fencing
        self.services_enabled = services
        self.customer_signup_enabled = customer_signup
        self.partner_app_enabled = partner_app

    def serialize(self):
        return {
            "geo_location_enabled": self.is_geo_location_enabled(),
            "google_places_enabled": self.is_google_places_enabled(),
            "geo_tracking_enabled": self.is_geo_tracking_enabled(),
            "partner_app_enabled": self.is_partner_app_enabled(),
            "customer_app_enabled": self.is_customer_app_enabled(),
            "admin_dashboard_enabled": self.is_admin_dashboard_enabled(),
            "image_upload_enabled": self.is_image_upload_enabled(),
            "geo_fencing_enabled": self.is_geo_fencing_enabled(),
            "services_enabled": self.is_services_enabled(),
            "customer_signup_enabled": self.is_customer_signup_enabled(),
            "partner_signup_enabled": self.is_partner_signup_enabled(),
        }