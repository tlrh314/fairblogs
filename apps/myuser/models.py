from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .managers import BloggerManager
import os


def get_blog_logo(instance, filename):
    """ Logo of the blog (website) """
    return os.path.join("static", "img",
        instance.blogname.replace(" ", ""), filename)

def get_blogger_logo(instance, filename):
    """ Logo of the blogger (person) """
    return os.path.join("static", "img",
        instance.affiliation.blogname.replace(" ", ""), filename)


@python_2_unicode_compatible
class AffiliatedBlog(models.Model):
    blogname = models.CharField(max_length=200)
    url = models.URLField()
    logo = models.ImageField(upload_to=get_blog_logo, blank=True, null=True)
    email = models.EmailField()

    facebook = models.URLField(_("Facebook"), null=True, blank=True)
    twitter = models.URLField(_("Twitter"), null=True, blank=True)
    instagram = models.URLField(_("Instagram"), null=True, blank=True)

    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="affilations_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("Affiliated Blog")
        verbose_name_plural = _("Affiliated Blogs")

    def __str__(self):
        return self.blogname


@python_2_unicode_compatible
class Blogger(AbstractBaseUser, PermissionsMixin):
    """ When referencing users, use: 'settings.AUTH_USER_MODEL' or 'get_user_model()' """
    email = models.EmailField(_("Email"), unique=True)
    first_name = models.CharField(_("Voornaam"), max_length=30)
    last_name = models.CharField(_("Achternaam"), max_length=30)

    affiliation = models.ForeignKey(AffiliatedBlog, related_name="blogger", on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(upload_to=get_blogger_logo, null=True, blank=True)

    is_active = models.BooleanField(_("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
        "active. Unselect this instead of deleting accounts."))
    is_staff = models.BooleanField(_("staff"), default=False,
        help_text=_("Designates whether the user can log into this admin site."))
    is_superuser = models.BooleanField(_("superuser"), default=False)

    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)

    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="blogger_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    objects = BloggerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "{0} {1}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email="no-reply@fairblogs.nl", **kwargs):
        """
        Sends an email to this User. Caution, from_email must contain domain name!
        """
        EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipients,
            bcc=["timohalbesma@gmail.com", "hello@fairblogs.nl"],
        ).send(fail_silently=False)

    def __str__(self):
        return self.get_full_name()
