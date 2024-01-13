from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User
from django.utils.translation import gettext_lazy as _


class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription étendu pour inclure le champ facultatif d'avatar.
    """
    avatar = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('avatar',)

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire en ajustant les libellés des champs.
        """
        super().__init__(*args, **kwargs)

        self.fields['avatar'].label = _('Avatar (optionnel)')
        self.fields['password2'].label = _('Confirmer mot de passe')


class AvatarUploadForm(forms.ModelForm):
    """
    Formulaire de téléchargement d'avatar pour la modification du profil.
    """
    class Meta:
        model = User
        fields = ['avatar']

    def clean_avatar(self):
        """
        Valide le champ avatar en s'assurant qu'il s'agit d'un fichier image.
        """
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if not avatar.content_type.startswith('image'):
                raise forms.ValidationError("Le fichier sélectionné n'est pas une image.")

        return avatar
