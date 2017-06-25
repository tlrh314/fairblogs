from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import ugettext_lazy as _

from .models import Blogger
from .models import AffiliatedBlog


@admin.register(AffiliatedBlog)
class AffiliatedBlogAdmin(admin.ModelAdmin):
    list_display = ("blogname", "email", "url" )
    search_fields = ("blogname", "email", "url" )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

admin.site.unregister(Group)


@admin.register(Blogger)
class BloggerAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    readonly_fields = ("last_login", "date_joined",)

    # form = BloggerChangeForm
    # add_form = BloggerCreationForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Blog Name"), {"fields": ("affiliation",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",
                                       "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2")}
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()
