from django.db import models
from django.utils import timezone
from utils.ReadableDateTime import generate_readable_date_time
from cloudinary.api import resource, delete_resources, NotFound
from cloudinary.uploader import upload
import cloudinary


class AdImageModel(models.Model):
    """ This model is used to stores the links to ad image links """
    tall_image_id = models.TextField(default="")
    tall_image_secure_url = models.TextField(default="")
    wide_image_id = models.TextField(default="")
    wide_image_secure_url = models.TextField(default="")
    last_updated = models.DateTimeField(default=timezone.now)

    def update_record(self, tall_image_id, tall_image_secure_url, wide_image_id, wide_image_secure_url):
        self.tall_image_id = tall_image_id
        self.tall_image_secure_url = tall_image_secure_url
        self.wide_image_id = wide_image_id
        self.wide_image_secure_url = wide_image_secure_url
        self.last_updated = timezone.now()

    def delete_tall_image(self):
        try:
            cl = delete_resources([self.tall_image_id])
            self.tall_image_id = ""
            self.tall_image_secure_url = ""
        except:
            pass

    def delete_wide_image(self):
        try:
            cl = delete_resources([self.wide_image_id])
            self.wide_image_id = ""
            self.wide_image_secure_url = ""
        except:
            pass

    def update_tall_image(self, image_file):
        #result = upload(image_file, height=400, width=200)
        try:
            cloudinary.config(
                cloud_name="janatarkalambackup",
                api_key="337747625353345",
                api_secret="XsW3rNnGzG7slxyKz2KS3MLNsSo"
            )
            result = upload(image_file)
            self.tall_image_id = result['public_id']
            self.tall_image_secure_url = result['secure_url']
        except cloudinary.api.Error:
            print("-----------------------------------------------")
            print("Got error in first config trying second")
            print("-----------------------------------------------")
            cloudinary.config(
                cloud_name="janatarkalam",
                api_key="158518893827718",
                api_secret="TPhvUo9kxFVeETYmSKvMCYlXMLc"
            )
            result = upload(image_file)
            self.tall_image_id = result['public_id']
            self.tall_image_secure_url = result['secure_url']
        except:
            raise

    def update_wide_image(self, image_file):
        #result = upload(image_file, height=400, width=200)
        try:
            cloudinary.config(
                cloud_name="janatarkalambackup",
                api_key="337747625353345",
                api_secret="XsW3rNnGzG7slxyKz2KS3MLNsSo"
            )
            result = upload(image_file)
            self.wide_image_id = result['public_id']
            self.wide_image_secure_url = result['secure_url']
        except cloudinary.api.Error:
            print("-----------------------------------------------")
            print("Got error in first config trying second")
            print("-----------------------------------------------")
            cloudinary.config(
                cloud_name="janatarkalam",
                api_key="158518893827718",
                api_secret="TPhvUo9kxFVeETYmSKvMCYlXMLc"
            )
            result = upload(image_file)
            self.wide_image_id = result['public_id']
            self.wide_image_secure_url = result['secure_url']
        except:
            raise

    def serialize(self):
        return {
            "id": self.id,
            "tall_image_id": self.tall_image_id,
            "tall_image_secure_url": self.tall_image_secure_url,
            "wide_image_id": self.wide_image_id,
            "wide_image_secure_url": self.wide_image_secure_url,
            "last_updated": generate_readable_date_time(self.last_updated)
        }