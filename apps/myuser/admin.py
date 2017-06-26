from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from django.utils.translation import ugettext_lazy as _

from .models import Blogger
from .models import AffiliatedBlog


@admin.register(AffiliatedBlog)
class AffiliatedBlogAdmin(admin.ModelAdmin):
    list_display = ("blogname", "email", "url" )
    search_fields = ("blogname", "email", "url" )
    readonly_fields = ( "date_created", "date_updated", "last_updated_by" )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

admin.site.unregister(Group)


@admin.register(Blogger)
class BloggerAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "affiliation", "is_active", "is_staff", "is_superuser")
    list_filter = ("affiliation", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name", "affiliation__blogname")
    ordering = ("email",)
    readonly_fields = ("last_login", "date_joined",)
    actions = ("confirm_new_user", )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "avatar")}),
        (_("Blog Name"), {"fields": ("affiliation",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",
                                       "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "affiliation", "avatar", "password1", "password2")}
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def confirm_new_user(self, request, queryset):
        for user in queryset:
            user.is_active = True
            user.save()
            current_site = get_current_site(request)
            subject = "Your account at {0} has been confirmed!".format(current_site.name)
            message = render_to_string("myuser/account_verified.html", {
                "user": user,
                "protocol": request.scheme,
                "domain": current_site.domain,
            })
            user.email_user(subject, message, from_email="no-reply@fairblogs.nl")


            content_type_pk = ContentType.objects.get_for_model(Blogger).pk
            LogEntry.objects.log_action(
                request.user.pk, content_type_pk, user.pk, str(user), CHANGE,
                change_message="Account confirmed by {0}.".format(request.user)
            )
        self.message_user(request, "Successfully confirmed: {0}.".format(user))
