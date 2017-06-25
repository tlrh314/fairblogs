from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required

from .models import ContactInfo
from .models import WelcomeMessage
from .models import PrivacyPolicy
from .forms import ContactForm
from ..blog.models import Post


def privacy_policy(request):
    pp = PrivacyPolicy.objects.all()
    if pp:
        policy = pp[0].policy
        last_updated = pp[0].last_updated
    else:
        policy = "Our privacy policy is still work in progress."
        last_updated = None
    return render(request, "pages/privacy_policy.html",
        {"privacy_policy": policy, "privacy_policy_last_update": last_updated })


def index(request):
    welcome = WelcomeMessage.objects.all()
    if welcome:
        welcome = welcome[0].text
    else:
        welcome = "Welcome at the API Alumnus Website!"

    #Filtering all posts on whether they are published, and picking the latest
    latest_post = Post.objects.filter(is_published=True).latest("date_created")
    latest_thesis = Degree.objects.filter(type="phd").latest("date_of_defence")

    return render(request, "pages/index.html", {"welcome_text": welcome, "latest_post": latest_post, "latest_thesis": latest_thesis})


def page_not_found(request):
    # TODO: passing contactinfo is given to all templates in context_processors.py.
    # The page_not_found method does not need to give contactinfo to template?
    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        webmaster_email_address = contactinfo[0].webmaster_email_address
    else:
        # Hardcoded in case ContactInfo has no instances.
        webmaster_email_address = "secr-astro-science@uva.nl"
    return render(request, "404.html", {"webmaster_email_address": webmaster_email_address})


def contact(request):
    form_class = ContactForm

    recipients = []
    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        secretariat = contactinfo[0].secretary_email_address
        recipients.append(secretariat)
    else:
        # Hardcoded in case ContactInfo has no instances.
        secretariat = "secr-astro-science@uva.nl"
        recipients.append(secretariat)


    if request.method == "POST":
        form = form_class(data=request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            if cc_myself:
                recipients.append(sender)

            # Caution, this breaks if there is no site.
            site_name = Site.objects.all()[0].name
            msg = "{0}\n\n".format(message)
            msg += "-------------------------------------------------\n\n"
            msg += "From: {0}\n".format(name)
            msg += "Email Address: {0}\n\n".format(sender)
            msg += "This message was automatically send from https://{0}/contact".format(site_name)

            email = EmailMessage(
                subject="Message from {0}/contact".format(site_name),
                body=msg,
                # Caution, from_email must contain domain name!
                from_email="no-reply@api-alumni.nl",
                to=recipients,
                bcc=["timohalbesma@gmail.com", "davidhendriks93@gmail.com" ],
                # Caution, reply_to header is already set by Postfix!
                # reply_to=list(secretariat),
                # headers={'Message-ID': 'foo'},
            )
            email.send(fail_silently=False)
            return HttpResponseRedirect("/thanks/")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})


def contact_success(request):
return render(request, "pages/thanks.html")
