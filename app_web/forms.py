from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from .models import Ticket, Review

from . import models


class TicketPostForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewPostForm(forms.ModelForm):
    #ticket_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Review
        #fields = ['ticket_id', 'rating', 'headline', 'body']
        fields = ['rating', 'headline', 'body']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
