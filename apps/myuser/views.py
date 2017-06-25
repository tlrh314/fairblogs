from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from .forms import SignUpForm
from .models import Blogger
from .tokens import account_activation_token

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate Your Account at {0}".format(current_site.name)
            message = render_to_string("myuser/account_activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            user.email_user(subject, message, from_email="no-reply@fairblogs.nl")

            return redirect("activation_sent")
    else:
        form = SignUpForm()
    return render(request, "myuser/signup.html", {"form": form})


def activation_sent(request):
    return render(request, "myuser/activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Blogger.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Blogger.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect("index")
    else:
        return render(request, "myuser/account_activation_invalid.html")
