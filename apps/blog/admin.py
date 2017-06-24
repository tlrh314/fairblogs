from django.contrib import admin

from .models import Tag
# from .models import Category
from .models import Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ( "date_created", "date_updated", "last_updated_by" )


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     readonly_fields = ( "date_created", "date_updated", "last_updated_by" )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated",)
    filter_horizontal = ("tags",)
