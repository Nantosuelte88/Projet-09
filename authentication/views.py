from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

from app_web.utils import resize_image
from .forms import AvatarUploadForm

from django.contrib import messages

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            if user.avatar:
                user.resize_image()

            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, 'Erreur lors de la création du ticket '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = forms.SignupForm()
    return render(request, 'authentication/signup.html', context={'form': form})


@login_required
def add_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)

        if not request.FILES:
            messages.error(request, "Veuillez sélectionner un fichier.")

        else:
            if form.is_valid():
                user = form.save(commit=False)

                # Redimensionnement de l'image
                if 'avatar' in request.FILES:
                    image_path = request.FILES['avatar']
                    if resize_image(image_path):
                        # Si le redimensionnement réussit, sauvegarder le modèle
                        user.save()
                        return redirect('feed')
                else:
                    messages.error(request, "view add_avatar")
                    messages.error(request, "Erreur lors du redimensionnement de l'image.")

            else:
                print('Form is not valid:', form.errors)

    else:
        form = AvatarUploadForm()

    return render(request, 'authentication/add_avatar.html', {'form': form})


@login_required
def update_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)

        if not request.FILES:
            return redirect('feed')
        else:
            if form.is_valid():
                user = form.save(commit=False)

                # Redimensionnement de l'image
                if 'avatar' in request.FILES:
                    image_path = request.FILES['avatar']
                    if resize_image(image_path):
                        # Si le redimensionnement réussit, sauvegarder le modèle
                        user.save()
                        return redirect('feed')
                else:
                    messages.error(request, "view update_avatar")
                    messages.error(request, "Erreur lors du redimensionnement de l'image.")

            else:
                messages.error(request, "Erreur lors de la mise à jour de l'avatar. "
                                        "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AvatarUploadForm()

    return render(request, 'authentication/update_avatar.html', {'form': form})


@login_required
def delete_avatar(request):
    user = request.user
    try:
        if user.avatar:
            user.avatar.delete()
            user.avatar = None
            user.save()
    except PermissionDenied as e:
        # Loggez l'erreur ou imprimez-la pour le débogage
        print(f"Erreur lors de la suppression de l'avatar : {e}")

    return redirect('feed')
