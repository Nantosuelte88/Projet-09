from django import forms
from .models import Ticket, Review

from . import models


class TicketPostForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewToTicketForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']

    ticket_id = forms.IntegerField(widget=forms.HiddenInput())

    def save(self, commit=True):
        ticket_id = self.cleaned_data['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)

        review_instance = super(ReviewToTicketForm, self).save(commit=False)
        review_instance.ticket = ticket

        if commit:
            review_instance.save()

        return review_instance


class TicketAndReviewForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    def save(self, commit=True):
        ticket_instance = super(TicketAndReviewForm, self).save(commit=False)
        ticket_instance.save()

        review_instance = Review.objects.create(
            ticket=ticket_instance,
            rating=self.cleaned_data['review_rating'],
            headline=self.cleaned_data['review_headline'],
            body=self.cleaned_data['review_body']
        )

        return review_instance
