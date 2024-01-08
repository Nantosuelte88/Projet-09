from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from .models import Ticket, Review
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html

from . import models


class CustomImagePreviewWidget(ClearableFileInput):
    template_name = 'app_web/widgets/custom_image_preview_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and hasattr(value, "url"):
            return format_html(
                '<img src="{}" alt="{}" class="img-form">{}</label>',
                value.url, value.name, html
            )
        return html


class TicketPostForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewPostForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'rating-radio'}),
        }

    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
                               required=True)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class RadioSelectWithInlineLabel(forms.RadioSelect):
    template_name = 'app_web/widgets/radio_select_inline_label.html'
