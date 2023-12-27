from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from .models import Ticket, Review

from . import models


class TicketPostForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewPostForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
