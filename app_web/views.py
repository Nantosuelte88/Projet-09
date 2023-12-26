from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TicketPostForm, \
    ReviewToTicketForm, TicketAndReviewForm
from .models import Ticket

from django.contrib import messages

from . import models


@login_required
def home(request):
    return render(request, 'app_web/home.html')


@login_required
def flux(request):
    tickets = Ticket.objects.all()
    return render(request, 'app_web/flux.html', {'tickets': tickets})


@login_required
def ticket_demand(request):
    if request.method == 'POST':
        form = TicketPostForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Ticket créé avec succès!')
            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la création du ticket '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = TicketPostForm()

    return render(request, 'app_web/ticket_page.html', {'form': form})


@login_required
def review_add(request):
    if request.method == 'POST':
        form = TicketAndReviewForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'TicketCritique créé avec succès!')
            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la création de la Critique. '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = TicketAndReviewForm()

    return render(request, 'app_web/review.html', {'form': form})


@login_required
def posts(request):
    tickets = Ticket.objects.all()
    return render(request, 'app_web/posts.html', {'tickets': tickets})


@login_required
def subscription(request):
    return render(request, 'app_web/subscription.html')
