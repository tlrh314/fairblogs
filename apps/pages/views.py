from __future__ import unicode_literals, absolute_import, division

from django.http import Http404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required

from .models import ContactInfo
from .models import PrivacyPolicy
from .models import AboutUs
from .forms import ContactForm
from ..blog.models import Post
from context_processors import contactinfo

def about(request):
    about = AboutUs.objects.all()
    if len(about) is 0:
        about = "Our apologies, the About Us page is still work in progress."
    elif len(about) == 1:
        about = about[0]
    else:
        raise Http404
    return render(request, "pages/aboutus.html",  {"info": about })


def contact(request):
    form_class = ContactForm

    recipients = []
    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        send_to = contactinfo[0].contact_email
        recipients.append(send_to)
    else:
        # Hardcoded in case ContactInfo has no instances.
        send_to = "hello@fairblogs.nl"
        recipients.append(send_to)

    if settings.DEBUG:
        recipients = []

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
                from_email="no-reply@fairblogs.nl",
                to=recipients,
                bcc=["timohalbesma@gmail.com", ], #"marcellawijngaarden@hotmail.com" ],
                # Caution, reply_to header is already set by Postfix!
                # reply_to=list(send_to),
                # headers={"Message-ID": "foo"},
            )
            email.send(fail_silently=False)
            return HttpResponseRedirect(reverse("contact_success"))
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})


def contact_success(request):
    return render(request, "pages/contact_success.html")


def privacy_policy(request):
    pp = PrivacyPolicy.objects.all()
    if len(pp) == 1:
        policy = pp[0].policy
        last_updated = pp[0].date_updated
    else:
        policy = "Our privacy policy is still work in progress."
        last_updated = None
    return render(request, "pages/privacy_policy.html",
        {"privacy_policy": policy, "privacy_policy_last_update": last_updated })

def page_not_found(request):
    # Info from context_processors seems unavailable. So we pass contactinfo.
    return render(request, "404.html", contactinfo(request))
