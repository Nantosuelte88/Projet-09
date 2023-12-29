from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ticket, Review, BlockedUser, UserFollows

from authentication.models import User


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'image', 'time_created')


admin.site.register(Ticket, TicketAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rating', 'headline', 'body','user', 'time_created')


admin.site.register(Review, ReviewAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'avatar')


admin.site.register(User, UserAdmin)


class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'blocked_user', 'can_access_tickets', 'can_access_reviews')


admin.site.register(BlockedUser, BlockedUserAdmin)


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')


admin.site.register(UserFollows, UserFollowsAdmin)