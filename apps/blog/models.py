import os

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tinymce.models import HTMLField


def get_post_image(instance, filename):
    """ Logo of the blog (website) """
    return os.path.join("static", "img", "bloggers", str(instance.author.blogger.blogname), "posts", filename)


@python_2_unicode_compatible
class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="category_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.category_name


@python_2_unicode_compatible
class Category(models.Model):
    category_name = models.CharField(max_length=200)

    last_updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="tags_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.category_name


@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name="post_changed_by", default=None)
    title = models.CharField(max_length=300)
    slug = models.SlugField(_("slug"), unique=True)
    teaser = HTMLField(_("Teaser"), blank=True, default="")
    image = models.ImageField(_("Teaser Photo"), upload_to=get_post_image, blank=True, null=True)

    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Published"), auto_now=True, blank=True, null=True)

    tags = models.ManyToManyField(Tag, help_text="Tags", blank=True)
    categories = models.ManyToManyField(Category, help_text="Categories", blank=True)

    featured = models.BooleanField(default=False,
        help_text="Should this post be shown in the featured list?")

    class Meta:
        ordering = ["-date_updated",]

    def publish(self):
        self.date_updated = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

    def __str__(self):
        return self.title
