from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketPostForm, ReviewPostForm
from .models import Ticket, Review, UserFollows, BlockedUser

from django.core.files.uploadedfile import SimpleUploadedFile

from authentication.models import User

from django.contrib import messages


@login_required
def feed(request):
    """
    Gère le flux des tickets et reviews à afficher pour l'utilisateur.
    """
    # Récupère les utilisateurs suivis
    following_users = request.user.following.all()

    # Tickets et Reviews des utilisateurs suivis
    tickets_followed = Ticket.objects.filter(user__in=following_users)
    reviews_followed = Review.objects.filter(user__in=following_users)

    # Tickets et reviews de l'utilisateur connecté
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    # Reviews en réponse aux tickets de l'utilisateur connecté
    reviews_in_response = Review.objects.filter(ticket__user=request.user)

    # Liste temporaire pour stocker les ID des reviews déjà ajoutées
    added_reviews_ids = set()

    for review in reviews_followed:
        added_reviews_ids.add(review.id)

    # Rassemble différents types de publications
    posts = [
                {'post': ticket, 'post_type': 'TICKET'} for ticket in tickets_followed
            ] + [
                {'post': review, 'post_type': 'REVIEW'} for review in reviews_followed
            ] + [
                {'post': review, 'post_type': 'REVIEW'} for review in reviews_in_response if
                review.id not in added_reviews_ids
            ] + [
                {'post': user_ticket, 'post_type': 'TICKET'} for user_ticket in user_tickets
            ] + [
                {'post': user_review, 'post_type': 'REVIEW'} for user_review in user_reviews
            ]

    # Trie les publications par ordre décroissant de création
    posts.sort(key=lambda x: x['post'].time_created, reverse=True)

    # Récupère les informations de notation pour l'affichage des étoiles en HTML
    for post in posts:
        if post['post_type'] == 'REVIEW':
            post['stars'] = {
                'filled_stars': range(post['post'].rating),
                'empty_stars': range(5 - post['post'].rating)
            }

        elif post['post_type'] == 'TICKET':
            reviews = post['post'].review_set.all()
            if reviews:
                average_rating = sum(review.rating for review in reviews) / len(reviews)
                post['stars'] = {
                    'filled_stars': range(int(average_rating)),
                    'empty_stars': range(int(5 - average_rating))
                }

    return render(request, 'app_web/feed.html', {'posts': posts})


@login_required
def ticket_demand(request):
    """
    Gère la création de tickets via un formulaire.
    """
    if request.method == 'POST':
        form = TicketPostForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            if ticket.image:
                ticket.resize_image()
            messages.success(request, 'Ticket créé avec succès!')
            return redirect('feed')
        else:
            messages.error(request, 'Erreur lors de la création du ticket '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = TicketPostForm()

    return render(request, 'app_web/ticket_page.html', {'form': form})


@login_required
def ticket_delete(request, ticket_id):
    """
    Gère la suppression d'un ticket via un formulaire (bouton).
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.user != ticket.user:
        messages.warning(request, 'Vous n\'êtes pas autorisé à supprimer cette critique!')
        return redirect('feed')

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Demande de critique supprimé avec succès!')

    return redirect('feed')


@login_required
def ticket_update(request, ticket_id):
    """
    Gère la modification d'un ticket avec possibilité de supprimer ou remplacer l'image.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.user != ticket.user:
        messages.warning(request, 'Vous n\'êtes pas autorisé à modifier cette critique!')
        return redirect('feed')
    else:
        form = TicketPostForm(request.POST or None, request.FILES or None, instance=ticket)

        context = {
            'form': form,
            'ticket': ticket,
        }

        if request.method == 'POST':
            if form.is_valid():
                new_image = form.cleaned_data.get('image')
                if new_image:
                    if isinstance(new_image, SimpleUploadedFile):
                        if ticket.image:
                            ticket.image.delete(save=False)
                        ticket.image = new_image

                ticket.user = request.user
                ticket.time_created = timezone.now()
                form.save()
                messages.success(request, 'Demande de critique modifié avec succès!')
                return redirect('feed')
            else:
                messages.error(request, 'Erreur lors de la modification de la critique. '
                                        'Veuillez corriger les erreurs dans le formulaire.')

    return render(request, 'app_web/ticket_page.html', context=context)


@login_required
def review_add(request, ticket_id):
    """
    Gère la création d'une review en réponse à un ticket via un formulaire.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # Vérifier si une critique existe déjà pour ce ticket
    existing_review = Review.objects.filter(ticket=ticket, user=request.user).first()

    if existing_review:
        messages.warning(request, 'Vous avez déjà créé une critique pour ce ticket.')
        return redirect('feed')

    if request.method == 'POST':
        form = ReviewPostForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Critique créé avec succès!')
            return redirect('feed')
        else:
            messages.error(request, 'Erreur lors de la création de la critique '
                                    'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ReviewPostForm(initial={'ticket_id': ticket.id})

    context = {
        'form': form,
        'ticket': ticket,
    }

    return render(request, 'app_web/review_edit.html', context=context)


@login_required
def review_delete(request, review_id):
    """
    Gère la suppression d'une review via un formulaire (bouton).
    """
    review = get_object_or_404(Review, pk=review_id)

    if request.user != review.user:
        messages.warning(request, 'Vous n\'êtes pas autorisé à supprimer cette critique!')
        return redirect('feed')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Critique supprimée avec succès!')

    return redirect('feed')


@login_required
def review_update(request, review_id):
    """
    Gère la modification d'une review.
    """
    review = get_object_or_404(Review, pk=review_id)
    ticket = review.ticket

    if request.user != review.user:
        messages.warning(request, 'Vous n\'êtes pas autorisé à modifier cette critique!')
        return redirect('feed')
    else:
        form = ReviewPostForm(request.POST or None, request.FILES or None, instance=review)
        context = {
            'form': form,
            'review': review,
            'ticket': ticket,
        }

        if request.method == 'POST':
            if form.is_valid():
                review.user = request.user
                review.ticket = ticket
                review.time_created = timezone.now()
                form.save()
                messages.success(request, 'Critique modifié avec succès!')
                return redirect('feed')
            else:
                messages.error(request, 'Erreur lors de la modification de la critique. '
                                        'Veuillez corriger les erreurs dans le formulaire.')

    return render(request, 'app_web/review_edit.html', context=context)


@login_required
def ticket_and_review(request):
    """
    Gère la création d'un ticket et d'une review en réponse à celui-ci.
    """
    ticket_form = TicketPostForm()
    review_form = ReviewPostForm()
    if request.method == 'POST':
        ticket_form = TicketPostForm(request.POST, request.FILES)
        review_form = ReviewPostForm(request.POST, request.FILES)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            if ticket.image:
                ticket.resize_image()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            messages.success(request, 'TicketCritique créé avec succès!')
            return redirect('feed')
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
    """
    Gère l'affichage des posts créés par l'utilisateur.
    """
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    posts = [{'post': user_ticket, 'post_type': 'TICKET'} for user_ticket in user_tickets] + \
            [{'post': user_review, 'post_type': 'REVIEW'} for user_review in user_reviews]

    posts.sort(key=lambda x: x['post'].time_created, reverse=True)

    for post in posts:
        if post['post_type'] == 'REVIEW':
            post['stars'] = {
                'filled_stars': range(post['post'].rating),
                'empty_stars': range(5 - post['post'].rating)
            }
        elif post['post_type'] == 'TICKET':
            reviews = post['post'].review_set.all()
            if reviews:
                average_rating = sum(review.rating for review in reviews) / len(reviews)
                post['stars'] = {
                    'filled_stars': range(int(average_rating)),
                    'empty_stars': range(int(5 - average_rating))
                }

    return render(request, 'app_web/posts.html', {'posts': posts})


@login_required
def subscription(request):
    """
    Gère les abonnements et les utilisateurs bloqués.

    Permet à l'utilisateur de suivre d'autres utilisateurs,
    de voir ses abonnés, et de gérer la liste d'utilisateurs bloqués.
    """
    # Récupération des utilisateurs suivis
    following_users = request.user.following.all()

    # Récupération des utilisateurs bloqués
    blocked_users = User.objects.filter(blocking_users__user=request.user, blocking_users__can_access_tickets=False)

    # Récupération des utilisateurs qui suivent l'utilisateur actuel
    followers = User.objects.filter(user_follows__followed_user=request.user)

    if request.method == 'POST':
        # Récupération du pseudo à suivre dans le formulaire
        username_to_follow = request.POST.get('username_to_follow')
        user_to_follow = User.objects.filter(username=username_to_follow).first()

        if user_to_follow:
            if user_to_follow == request.user:
                # Message d'erreur si l'utilisateur essaie de se suivre lui-même
                messages.error(request, f"Vous ne pouvez pas vous suivre vous-même ;)")
            else:
                # Vérifier si l'utilisateur cible est bloqué
                if BlockedUser.objects.filter(user=request.user, blocked_user=user_to_follow).exists():
                    messages.error(request, f"Vous ne pouvez pas suivre un utilisateur bloqué.")
                elif BlockedUser.objects.filter(user=user_to_follow, blocked_user=request.user).exists():
                    # Même message d'erreur que celui d'un utilisateur inexistant,
                    # quand l'utilisateur est bloqué, à changer au besoin
                    messages.error(request, f"L'utilisateur '{username_to_follow}' n'existe pas.")
                else:
                    # Gestion du suivi de l'utilisateur cible
                    user_follow, created = UserFollows.objects.get_or_create(user=request.user,
                                                                             followed_user=user_to_follow)
                    if created:
                        messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
                    else:
                        messages.success(request, f"Vous suivez déjà {user_to_follow.username}.")
        else:
            # Message d'erreur si l'utilisateur cible n'existe pas
            messages.error(request, f"L'utilisateur '{username_to_follow}' n'existe pas.")

    context = {'following_users': following_users, 'blocked_users': blocked_users, 'followers': followers}
    messages.success(request, '')
    return render(request, 'app_web/subscription.html', context)


@login_required
def unfollow(request):
    """
    Gère le désabonnement à un utilisateur.
    """
    if request.method == 'POST':
        user_to_unfollow_id = request.POST.get('user_to_unfollow')
        user_to_unfollow = get_object_or_404(User, id=user_to_unfollow_id)
        UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()

    return redirect('subscription')


@login_required
def block_user(request):
    """
    Gère le blocage d'un utilisateur.
    """
    if request.method == 'POST':
        # Récupère l'ID de l'utilisateur à bloquer et obtient l'objet à bloquer.
        user_to_block_id = request.POST.get('user_to_block')
        user_to_block = get_object_or_404(User, id=user_to_block_id)

        # Supprime toute relation de suivi entre l'utilisateur bloquant et l'utilisateur bloqué.
        if UserFollows.objects.filter(user=user_to_block, followed_user=request.user).exists():
            UserFollows.objects.filter(user=user_to_block, followed_user=request.user).delete()

        if UserFollows.objects.filter(user=request.user, followed_user=user_to_block).exists():
            UserFollows.objects.filter(user=request.user, followed_user=user_to_block).delete()

        # Crée une nouvelle entrée dans la table BlockedUser pour enregistrer le blocage.
        BlockedUser.objects.create(user=request.user, blocked_user=user_to_block)

        # Supprimer les reviews de l'utilisateur bloqué en réponse aux tickets de l'utilisateur bloquant
        user_reviews_to_delete = Review.objects.filter(user=user_to_block, ticket__user=request.user)
        user_reviews_to_delete.delete()

        # Supprimer les reviews de l'utilisateur bloquant en réponse aux tickets de l'utilisateur bloqué
        blocked_user_tickets = Ticket.objects.filter(user=user_to_block)
        blocked_user_reviews_to_delete = Review.objects.filter(user=request.user, ticket__in=blocked_user_tickets)
        blocked_user_reviews_to_delete.delete()

        messages.success(request, f"Vous avez bloqué l'utilisateur {user_to_block.username}.")

    return redirect('subscription')


@login_required
def unblock_user(request):
    """
    Gère le déblocage d'un utilisateur
    """
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
    """
    Permet l'affichage de la page de mentions légales
    """
    return render(request, 'app_web/mentions_legales.html')
