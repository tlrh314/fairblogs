import os.path

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from tinymce.models import HTMLField


def place_welcome_photo(instance, filename):
    return os.path.join("uploads", filename)

def get_company_logo(instance, filename):
    """ Logo of the owner websites (website) """
    return os.path.join("static", "img", "logos", filename)

def validate_only_one_instance(obj):
    """ Allow only one instance of a model to be created, in this case WelcomeMessage and ContactInfo """
    model = obj.__class__
    if (model.objects.count() > 0 and obj.id != model.objects.get().id):
        raise ValidationError("Errror: only 1 instance of {0} is allowed and it already exists.".format(model.__name__))


class PrivacyPolicy(models.Model):
    policy = HTMLField(verbose_name=_("Privacy Policy"), blank=True)

    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="privacy_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("Privacy Policy")
        verbose_name_plural = _("Privacy Policy")

    def clean(self):
        validate_only_one_instance(self)


class Disclaimer(models.Model):
    policy = HTMLField(verbose_name=_("Disclaimer"), blank=True)

    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="disclaimer_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("Disclaimer")
        verbose_name_plural = _("Disclaimer")

    def clean(self):
        validate_only_one_instance(self)


class AboutUs(models.Model):
    about = HTMLField(verbose_name=_("About Us"), blank=True, help_text='Bovenste gedeelte over FairBlogs op de about pagina.')
    about_below = HTMLField(verbose_name=_("About Us"), blank=True, help_text='Onderste gedeelte over FairBlogs op de about pagina.')

    about_fairfrog = HTMLField(verbose_name=_("About Fairfrog"), blank=True)
    url_fairfrog = models.URLField(help_text='Website url', blank=True)
    logo_fairfrog = models.ImageField(upload_to=get_company_logo, blank=True, null=True)

    about_sociii = HTMLField(verbose_name=_("About Sociii"), blank=True)
    url_sociii = models.URLField(help_text='Website url', blank=True)
    logo_sociii = models.ImageField(upload_to=get_company_logo, blank=True, null=True)

    about_projectcece = HTMLField(verbose_name=_("About Project Cece"), blank=True)
    url_projectcece = models.URLField(help_text='Website url', blank=True)
    logo_projectcece = models.ImageField(upload_to=get_company_logo, blank=True, null=True)

    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="aboutus_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = _("About Us")
        verbose_name_plural = _("About Us")

    def clean(self):
        validate_only_one_instance(self)


class ContactInfo(models.Model):
    contact_email = models.EmailField(_("Contact Email"))
    webmaster_email = models.EmailField(_("Webmaster Email"))
    address = models.CharField(_("Address"), max_length=256)
    postbox = models.CharField(_("PO Box"), max_length=256)
    phone = models.CharField(_("Phone Number"), max_length=20)

    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="contactinfo_changed_by", )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Last Changed"), auto_now=True)

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def clean(self):
        validate_only_one_instance(self)
