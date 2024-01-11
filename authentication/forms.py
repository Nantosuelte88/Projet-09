from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['avatar'].label = _('Avatar (optionnel)')
        self.fields['password2'].label = _('Confirmer mot de passe')


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if not avatar.content_type.startswith('image'):
                raise forms.ValidationError("Le fichier sélectionné n'est pas une image.")

        return avatar
