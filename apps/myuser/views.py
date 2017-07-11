from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from .forms import SignUpForm
from .forms import CreateAffiliationForm
from .forms import SelectAffiliationForm
from .forms import EditBloggerForm
from .forms import EditAffiliationForm
from .models import Blogger
from .models import AffiliatedBlog
from .tokens import account_activation_token
from context_processors import contactinfo

def signup(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activeer jouw account op {0}".format(current_site.name)
            message = render_to_string("myuser/account_activation_email.html", {
                "user": user,
                "protocol": request.scheme,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            user.email_user(subject, message, from_email="no-reply@fairblogs.nl")

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(Blogger).pk
            LogEntry.objects.log_action(
                user.pk, content_type_pk, user.pk, str(user), CHANGE,
                change_message="User signed up."
            )

            # Redirect user to template
            if form.cleaned_data["affiliation"]:
                return redirect("activation_sent")
            else:
                request.session["new_user_pk"] = user.pk
                return redirect("new_affiliation")
    else:
        form = SignUpForm()
    return render(request, "myuser/signup.html", {"form": form})


def new_affiliation(request):
    if request.method == "POST":
        user = get_object_or_404(Blogger, pk=request.session.get("new_user_pk", None))
        form = CreateAffiliationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            affiliation = form.save(commit=False)
            affiliation.save()

            user.affiliation = affiliation
            user.save()

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(AffiliatedBlog).pk
            LogEntry.objects.log_action(
                user.pk, content_type_pk, affiliation.pk, str(affiliation), CHANGE,
                change_message="New affiliation created via signup form."
            )

            content_type_pk = ContentType.objects.get_for_model(Blogger).pk
            LogEntry.objects.log_action(
                user.pk, content_type_pk, user.pk, str(user), CHANGE,
                change_message="Added new affiliation: {0}.".format(affiliation)
            )

            return redirect("activation_sent")
    else:
        form = CreateAffiliationForm()
    return render(request, "myuser/new_affiliation.html", {"form": form})


@login_required
def set_affiliation(request):
    if request.method == "POST":
        form = SelectAffiliationForm(data=request.POST)
        if form.is_valid():
            which_blog = form.cleaned_data.get("which_blog", None)
            if not which_blog:
                request.session["new_user_pk"] = request.user.pk
                return redirect("new_affiliation")
            else:
                request.user.affiliation = which_blog
                request.user.save()
                return redirect("blogs:submit")
    else:
        form = SelectAffiliationForm()

    return render(request, "myuser/set_affiliation.html", { "form": form })


def activation_sent(request):
    return render(request, "myuser/activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Blogger.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Blogger.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Only confirm email and inform user via message
        user.email_confirmed = True
        # user.is_active = True
        # login(request, user)
        # messages.success(request, "Your account has succesfully been activated.")
        user.save()

        # Add record to LogEntry
        content_type_pk = ContentType.objects.get_for_model(Blogger).pk
        LogEntry.objects.log_action(
            user.pk, content_type_pk, user.pk, str(user), CHANGE,
            change_message="Email address confirmed by user."
        )

        # Inform site management that account now needs to be activated
        current_site = get_current_site(request)
        message = render_to_string("myuser/admin_activation_email.html", {
            "user": user,
            "user_email": user.email,
            "protocol": request.scheme,
            "domain": current_site.domain,
        })
        email = EmailMessage(
            subject="Activeer nieuwe gebruiker op {0}".format(current_site.name),
            body=message,
            # Caution, from_email must contain domain name!
            from_email="no-reply@fairblogs.nl",
            to=[ contactinfo(None)["contactinfo"].webmaster_email, ],
            bcc=["timohalbesma@gmail.com", ]
        )
        email.send(fail_silently=False)

        # return redirect("blogs:index")
        return redirect("email_validated")
    else:
        return render(request, "myuser/account_activation_invalid.html")


def email_validated(request):
    return render(request, "myuser/email_validated.html")


@login_required
def update_blogger(request):
    if request.method == "POST":
        form = EditBloggerForm(data=request.POST, instance=get_object_or_404(Blogger, pk=request.user.pk), files=request.FILES)
        if form.is_valid():
            user = form.save()

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(Blogger).pk
            LogEntry.objects.log_action(
                user.pk, content_type_pk, user.pk, str(user), CHANGE,
                change_message="User updated profile via website."
            )

            return redirect("show_blogger")
    else:
        form = EditBloggerForm(instance=get_object_or_404(Blogger, pk=request.user.pk))
    return render(request, "myuser/update_profile.html", {"form": form})


@login_required
def show_blogger(request):
    return render(request, "myuser/show_blogger.html")


@login_required
def update_affiliation(request):
    if request.method == "POST":
        form = EditAffiliationForm(data=request.POST, instance=get_object_or_404(AffiliatedBlog, pk=request.user.affiliation.pk), files=request.FILES)
        if form.is_valid():
            affiliation = form.save()

            # Add record to LogEntry
            content_type_pk = ContentType.objects.get_for_model(AffiliatedBlog).pk
            LogEntry.objects.log_action(
                request.user.pk, content_type_pk, affiliation.pk, str(affiliation), CHANGE,
                change_message="Affiliation updated profile via website."
            )

            return redirect("show_affiliation")
    else:
        form = EditAffiliationForm(instance=get_object_or_404(AffiliatedBlog, pk=request.user.affiliation.pk))
    return render(request, "myuser/update_affiliation.html", {"form": form})


@login_required
def show_affiliation(request):
    return render(request, "myuser/show_affiliation.html")


def all_bloggers(request):
    affiliation__bloggers = list()
    for blog in AffiliatedBlog.objects.all().exclude(blogname__in=["Project Cece", "FairFrog", "Sociii"]).order_by("blogname"):
        affiliation__bloggers.append(Blogger.objects.filter(affiliation=blog).order_by("last_name", "first_name"))

    return render(request, "myuser/all_bloggers.html", { "affiliation__bloggers": affiliation__bloggers })
