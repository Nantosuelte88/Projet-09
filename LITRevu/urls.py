from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

import authentication.views
import app_web.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('add_avatar/', authentication.views.add_avatar, name="add_avatar"),
    path('update_avatar/', authentication.views.update_avatar, name='update_avatar'),
    path('delete_avatar/', authentication.views.delete_avatar, name='delete_avatar'),
    path('home/', app_web.views.home, name='home'),
    path('feed/', app_web.views.feed, name='feed'),
    path('ticket_page/', app_web.views.ticket_demand, name='ticket'),
    path('ticket/<int:ticket_id>/delete/', app_web.views.ticket_delete, name='ticket_delete'),
    path('ticket/<int:ticket_id>/update/', app_web.views.ticket_update, name='ticket_update'),
    path('ticket_review/', app_web.views.ticket_and_review, name='ticketreview'),
    path('review/<int:ticket_id>/', app_web.views.review_add, name='review'),
    path('review/<int:review_id>/delete/', app_web.views.review_delete, name='review_delete'),
    path('review/<int:review_id>/update/', app_web.views.review_update, name='review_update'),
    path('posts/', app_web.views.posts_view, name='posts'),
    path('subscription/', app_web.views.subscription, name='subscription'),
    path('unfollow/', app_web.views.unfollow, name='unfollow'),
    path('block_user/', app_web.views.block_user, name='block_user'),
    path('unblock_user/', app_web.views.unblock_user, name='unblock_user'),
    path('mentions_legales/', app_web.views.legal_mention, name='mentions_legales'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
