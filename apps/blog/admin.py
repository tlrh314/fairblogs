from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from .models import Tag
from .models import Post
# from .models import Category


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ( "date_created", "date_updated", "last_updated_by" )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     readonly_fields = ( "date_created", "date_updated", "last_updated_by" )

#    def save_model(self, request, obj, form, change):
#        obj.last_updated_by = request.user
#        obj.save()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated",)
    list_display = ("title", "author", "get_affiliation", "date_updated" )
    search_fields = ("title", "author", "teaser")
    list_filter = ("is_published",)
    filter_horizontal = ("tags",)
    actions = ("publish", "unpublish" )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def get_affiliation(self, obj):
        return obj.author.affiliation
    get_affiliation.short_description = "Affiliation"

    def publish(self, request, queryset):
        for post in queryset:
            post.publish()

            content_type_pk = ContentType.objects.get_for_model(Post).pk
            LogEntry.objects.log_action(
                request.user.pk, content_type_pk, post.pk, str(post), CHANGE,
                change_message="Set status to 'Published'"
            )
        self.message_user(request, "Post successfully published.")
    publish.short_description = "Publish selected post"

    def unpublish(self, request, queryset):
        for post in queryset:
            post.unpublish()

            content_type_pk = ContentType.objects.get_for_model(Post).pk
            LogEntry.objects.log_action(
                request.user.pk, content_type_pk, post.pk, str(post), CHANGE,
                change_message="Set status to 'Unpublisheded'"
            )
        self.message_user(request, "Post successfully unpublished.")
    unpublish.short_description = "Unpublish selected post"
