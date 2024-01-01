from PIL import Image
import os
from django.db.models import Q
from .models import Review, Ticket

MAX_HEIGHT = 800


def resize_image(image_path):
    try:
        with Image.open(image_path) as image:
            image.thumbnail((image.width, MAX_HEIGHT))
            image.save(image_path)
        return True
    except Exception as e:
        print(f"Erreur lors du redimensionnement de l'image : {e}")
        return False


def get_star_rating(rating):
    return '★' * rating + '☆' * (5 - rating)


def get_users_viewable_reviews(user):
    following_users = user.following.all()
    reviews_followed = Review.objects.filter(user__in=following_users).values_list('id', flat=True)
    reviews_in_response = Review.objects.filter(ticket__user=user).values_list('id', flat=True)
    return list(reviews_followed) + list(reviews_in_response)


def get_users_viewable_tickets(user):
    following_users = user.following.all()
    tickets_followed = Ticket.objects.filter(user__in=following_users)
    return list(tickets_followed)