from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User


class SignupForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('avatar',)


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
