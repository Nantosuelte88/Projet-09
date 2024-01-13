from django import forms
from .models import Ticket, Review
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput


class CustomImageWidget(ClearableFileInput):
    """
    Widget personnalisé pour l'affichage de la partie image d'un formulaire de ticket.
    """
    def render(self, name, value, attrs=None, renderer=None):
        template = (
            '<br>'
            '<img src="%(image_url)s" alt="image actuelle de votre ticket"><br><br>'
            '<span class="img-delete">'
            '<label for="%(id)s-clear_id">Supprimer l\'image </label>'
            '<input type="checkbox" name="%(name)s-clear" id="%(id)s-clear_id">'
            '</span><br><br>'
            '<label for="%(id)s">Modifier l\'image</label><br>'
            '<input type="%(type)s" name="%(name)s" accept="%(accept)s" id="%(id)s">'
        )

        return mark_safe(template % {
            'id': attrs['id'],
            'name': name,
            'current_value': f'<a href="{value.url}">{value.name}</a>' if value else 'Aucune',
            'type': self.input_type,
            'accept': self.attrs.get('accept', 'image/*'),
            'image_url': value.url if value else '',
        })


class TicketPostForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification de tickets.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.image:
            self.fields['image'].widget = CustomImageWidget()

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
        }

    image = forms.ImageField(widget=forms.ClearableFileInput(), required=False)


class ReviewPostForm(forms.ModelForm):
    """
    Formulaire pour la création de critiques associées à un ticket.
    """
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'rating-radio'}),
        }
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaire',
        }

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
                               required=True)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


