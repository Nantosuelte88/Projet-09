from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.avatar)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.avatar.path)
