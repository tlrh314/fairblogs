import os
import re

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField


def get_post_image(instance, filename):
    """Logo of the blog (website)"""

    fnamesplit = filename.split(".")
    filename = "".join(fnamesplit[:-1])
    extension = fnamesplit[-1]
    return os.path.join(
        "static",
        "img",
        re.compile(r"[\W_]+").sub("", instance.author.affiliation.blogname),
        re.compile(r"[\W_]+").sub("", filename) + "." + extension,
    )


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="tag_changed_by",
    )
    date_created = models.DateTimeField(_("Date/Time Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date/Time Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="post_written_by",
        default=None,
    )
    title = models.CharField(_("Titel"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    teaser = HTMLField(
        _("Teaser"),
        blank=True,
        default="Inleiding/teaser voor je blogpost van max. 750 karakters",
        max_length=750,
    )
    image = models.ImageField(
        _("Teaser foto"), upload_to=get_post_image, blank=True, null=True
    )
    url = models.URLField(max_length=300)
    date_created = models.DateTimeField(
        _("Post is gepubliceerd op"), default=timezone.now
    )

    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(
        default=False, help_text="Should this post be shown in the featured list?"
    )

    tags = models.ManyToManyField(Tag, help_text="Tags", blank=True)
    # categories = models.ManyToManyField(Category, help_text="Categories", blank=True)

    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="post_changed_by",
    )
    # date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    date_updated = models.DateTimeField(_("Date Published"), blank=True, null=True)
    popularity = models.IntegerField(default=0)

    class Meta:
        ordering = [
            "-date_created",
        ]

    def publish(self):
        self.date_updated = timezone.now()
        self.is_published = True
        self.save()

    def unpublish(self):
        self.date_updated = None
        self.is_published = False
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
