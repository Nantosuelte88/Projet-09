from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TicketPostForm, ReviewPostForm
from .models import Ticket, Review

from django.contrib import messages

from . import models


@login_required
def home(request):
    user = request.user
    context = {
        'username': user.username,
        'avatar': user.avatar.url if user.avatar else None,
    }
    return render(request, 'app_web/home.html', context=context)


@login_required
def flux(request):
    tickets = Ticket.objects.all()
    return render(request, 'app_web/flux.html', {'tickets': tickets})


@login_required
def ticket_demand(request):
    if request.method == 'POST':
        form = TicketPostForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            print(ticket.image.path)
            ticket.resize_image()
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
        form = ReviewPostForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Critique créé avec succès!')
            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la création de la critique '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ReviewPostForm()

    return render(request, 'app_web/review.html', {'review_add_form': form})


@login_required
def ticket_and_review(request):
    ticket_form = TicketPostForm()
    review_form = ReviewPostForm()
    if request.method == 'POST':
        ticket_form = TicketPostForm(request.POST)
        review_form = ReviewPostForm(request.POST, request.FILES)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'TicketCritique créé avec succès!')
            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la création de la Critique. '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    # FAIRE UN ELSE ??
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }

    return render(request, 'app_web/ticket_review.html', context=context)


@login_required
def posts_view(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    #user_reviews = Review.objects.filter(ticket__user=request.user)    ??

    context = {
        'user_tickets' : user_tickets,
        'user_reviews' : user_reviews,
    }
    return render(request, 'app_web/posts.html', context=context)


@login_required
def subscription(request):
    return render(request, 'app_web/subscription.html')
