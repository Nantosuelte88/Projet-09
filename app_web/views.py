from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketPostForm, ReviewPostForm
from .models import Ticket, Review, UserFollows, BlockedUser
from .utils import get_star_rating

from authentication.models import User

from django.contrib import messages

from . import models


@login_required
def home(request):
    user = request.user
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    context = {
        'username': user.username,
        'avatar': user.avatar.url if user.avatar else None,
        'tickets': tickets,
        'reviews': reviews,
    }
    return render(request, 'app_web/home.html', context=context)


@login_required
def flux(request):
    following_users = request.user.following.all()

    tickets_followed = Ticket.objects.filter(user__in=following_users)
    reviews_followed = Review.objects.filter(user__in=following_users)
    reviews_in_response = Review.objects.filter(ticket__user=request.user)

    flux_content = list(tickets_followed) + list(reviews_followed) + list(reviews_in_response)
    flux_content.sort(key=lambda x: x.time_created, reverse=True)

    return render(request, 'app_web/flux.html', {'flux_content': flux_content})


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
def review_add(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # Vérifier si une critique existe déjà pour ce ticket
    existing_review = Review.objects.filter(ticket=ticket, user=request.user).first()

    if existing_review:
        messages.warning(request, 'Vous avez déjà créé une critique pour ce ticket.')
        return redirect('home')

    if request.method == 'POST':
        form = ReviewPostForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Critique créé avec succès!')
            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la création de la critique '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ReviewPostForm(initial={'ticket_id': ticket.id})

    context = {
        'form': form,
        'ticket': ticket,
    }

    return render(request, 'app_web/review.html', context=context)


@login_required
def review_delete(request, review_id):
    print(f"Deleting review with ID: {review_id}")
    review = get_object_or_404(Review, pk=review_id)

    if request.user != review.user:
        messages.warning(request, 'Vous n\'êtes pas autorisé à supprimer cette critique!')
        return redirect('flux')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Critique supprimé avec succès!')

    #context = {
    #    'review': review,
    #}

    return redirect('flux')
    #return render(request, 'app_web/review_delete.html', context=context)


@login_required
def review_update(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.user != review.user:
        messages.warning(request,'Vous n\'êtes pas autorisé à modifier cette critique!')
        return redirect('flux')

    if request.method == 'POST':
        form = ReviewPostForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Critique modifié avec succès!')
            return redirect('flux')
        else:
            messages.error(request, 'Erreur lors de la modification de la critique. '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ReviewPostForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'ticket_id': review.ticket,
    }

    return render(request, 'app_web/review.html', context=context)

@login_required
def ticket_and_review(request):
    ticket_form = TicketPostForm()
    review_form = ReviewPostForm()
    if request.method == 'POST':
        ticket_form = TicketPostForm(request.POST, request.FILES)
        review_form = ReviewPostForm(request.POST, request.FILES)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            ticket.resize_image()

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

    context = {
        'user_tickets': user_tickets,
        'user_reviews': user_reviews,
    }
    return render(request, 'app_web/posts.html', context=context)


@login_required
def subscription(request):
    following_users = request.user.following.all()
    blocked_users = User.objects.filter(blocking_users__user=request.user, blocking_users__can_access_tickets=False)
    followers = User.objects.filter(user_follows__followed_user=request.user)

    if request.method == 'POST':
        username_to_follow = request.POST.get('username_to_follow')
        user_to_follow = User.objects.filter(username=username_to_follow).first()

        if user_to_follow:
            # Vérifier si l'utilisateur cible est bloqué
            if BlockedUser.objects.filter(user=request.user, blocked_user=user_to_follow).exists():
                messages.error(request, f"Vous ne pouvez pas suivre un utilisateur bloqué.")
            elif BlockedUser.objects.filter(user=user_to_follow, blocked_user=request.user).exists():
                # Même message d'erreur que quand l'utilisateur n'existe pas, à changer au besoin
                messages.error(request, f"L'utilisateur '{username_to_follow}' n'existe pas.")
            else:
                # Toggle du suivi de l'utilisateur
                user_follow, created = UserFollows.objects.get_or_create(user=request.user,
                                                                         followed_user=user_to_follow)
                if created:
                    messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
                else:
                    messages.success(request, f"Vous ne suivez plus {user_to_follow.username}.")
        else:
            messages.error(request, f"L'utilisateur '{username_to_follow}' n'existe pas.")

    context = {'following_users': following_users, 'blocked_users': blocked_users, 'followers': followers}
    messages.success(request, '')
    return render(request, 'app_web/subscription.html', context)



@login_required
def unfollow(request):
    if request.method == 'POST':
        user_to_unfollow_id = request.POST.get('user_to_unfollow')
        user_to_unfollow = get_object_or_404(User, id=user_to_unfollow_id)
        UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()

    return redirect('subscription')


@login_required
def block_user(request):
    if request.method == 'POST':
        user_to_block_id = request.POST.get('user_to_block')
        user_to_block = get_object_or_404(User, id=user_to_block_id)

        if UserFollows.objects.filter(user=user_to_block, followed_user=request.user).exists():
            UserFollows.objects.filter(user=user_to_block, followed_user=request.user).delete()
            messages.success(request, f"Il vous suivait {user_to_block.username}.")

        else:
            messages.success(request, f"Il ne vous suivait pas {user_to_block.username}.")

        if UserFollows.objects.filter(user=request.user, followed_user=user_to_block).exists():
            UserFollows.objects.filter(user=request.user, followed_user=user_to_block).delete()
            messages.success(request, f"Vous ne suivez plus {user_to_block.username}.")

        else:
            messages.success(request, f"Vous ne suiviez pas {user_to_block.username}.")

        BlockedUser.objects.create(user=request.user, blocked_user=user_to_block)
        messages.success(request, f"Vous avez bloqué l'utilisateur {user_to_block.username}.")

    return redirect('subscription')


@login_required
def unblock_user(request):
    if request.method == 'POST':
        user_to_unblock_id = request.POST.get('user_to_unblock')
        user_to_unblock = get_object_or_404(User, id=user_to_unblock_id)

        # Vérifier si l'utilisateur est bloqué
        if BlockedUser.objects.filter(user=request.user, blocked_user=user_to_unblock).exists():
            # Supprimer l'entrée correspondante dans la table BlockedUser
            BlockedUser.objects.filter(user=request.user, blocked_user=user_to_unblock).delete()

    return redirect('subscription')


@login_required
def legal_mention(request):
    return render(request, 'app_web/mentions_legales.html')