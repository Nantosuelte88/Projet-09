from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

from PIL import Image


class Ticket(models.Model):
    """
    Modèle représentant un ticket dans l'application.

    Attributes:
        - title (CharField): Le titre du ticket.
        - description (TextField): La description détaillée du ticket.
        - user (ForeignKey): L'utilisateur associé à ce ticket.
        - image (ImageField): L'image attachée au ticket.
        - time_created (DateTimeField) : La date et l'heure de création du ticket.
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        """
        Redimensionne l'image attachée au ticket à la taille maximale spécifiée.

        Utilise la bibliothèque PIL pour redimensionner l'image.
        """
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Modèle représentant une critique associée à un ticket.

    Attributes:
    - ticket (ForeignKey): Le ticket associé à la critique.
    - rating (PositiveSmallIntegerField) : La note de la critique (entre 0 et 5).
    - headline (CharField) : Le titre de la critique.
    - body (TextField): Le contenu détaillé de la critique.
    - user (ForeignKey): L'utilisateur qui a écrit la critique.
    - time_created (DateTimeField) : La date et l'heure de création de la critique.
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    # modification de body, pour passer de CharField à TextField
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class BlockedUser(models.Model):
    """
    Modèle représentant un utilisateur bloqué par un autre utilisateur.

    Attributes:
    - user (ForeignKey) : L'utilisateur qui effectue le blocage.
    - blocked_user (ForeignKey) : L'utilisateur qui est bloqué.
    - can_access_tickets (BooleanField) : Indique si l'utilisateur bloqué peut accéder aux tickets.
    - can_access_reviews (BooleanField) : Indique si l'utilisateur bloqué peut accéder aux critiques.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_users'
    )

    blocked_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocking_users'
    )

    can_access_tickets = models.BooleanField(default=False)
    can_access_reviews = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'blocked_user', )


class UserFollows(models.Model):
    """
    Modèle représentant un suivi d'utilisateur.

    Attributes:
    - user (ForeignKey): L'utilisateur qui effectue le suivi.
    - followed_user (ForeignKey) : L'utilisateur suivi.

    Meta:
    - unique_together (tuple) : Assure qu'il n'y a qu'une seule instance de ce modèle
      pour chaque paire unique d'utilisateur et d'utilisateur suivi.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_follows')

    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        unique_together = ('user', 'followed_user', )
