from django.db import models
from django.contrib.auth.models import AbstractUser
from app_web.models import UserFollows
from PIL import Image


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé étendant la classe AbstractUser.

    Ajoute les champs 'following' pour gérer les abonnements et 'avatar' pour stocker les avatars des utilisateurs.
    """
    following = models.ManyToManyField('self', through=UserFollows)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        """
        Redimensionne l'image de l'utilisateur pour respecter les dimensions maximales définies.
        """
        if self.avatar and self.avatar.storage.exists(self.avatar.name):
            image = Image.open(self.avatar)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.avatar.path)
