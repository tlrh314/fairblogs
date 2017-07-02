from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from context_processors import contactinfo
from .views import signup
from .views import new_affiliation
from .views import activation_sent
from .views import activate
from .views import email_validated
from .views import update_blogger
from .views import show_blogger
from .views import update_affiliation
from .views import show_affiliation

urlpatterns = [
    url(r"^login/$", auth_views.LoginView.as_view(
        template_name="myuser/login.html"
        ), name="login"
    ),
    url(r"^logout/$", auth_views.LogoutView.as_view(
        template_name="myuser/logged_out.html"
        ), name="logout"
    ),

    url(r"^password_change/$", auth_views.PasswordChangeView.as_view(
        template_name="myuser/password_change_form.html",
        success_url = reverse_lazy("site_password_change_done")
        ), name="site_password_change"
    ),
    url(r"^password_change/done/$", auth_views.PasswordChangeDoneView.as_view(
        template_name="myuser/password_change_done.html",
        ), name="site_password_change_done"
    ),
    url(r"^password_reset/$", auth_views.PasswordResetView.as_view(
            template_name="myuser/password_reset_form.html",
            extra_context = {
                "phone_formatted": contactinfo(None)["phone_formatted"],
                "contact_email": contactinfo(None)["contactinfo"].contact_email,
            },
            email_template_name="myuser/password_reset_email.html",
            extra_email_context = {
                "phone_formatted": contactinfo(None)["phone_formatted"],
                "contact_email": contactinfo(None)["contactinfo"].contact_email,
            },
            success_url = reverse_lazy("site_password_reset_done")
        ), name="site_password_reset"
    ),
    url(r"^password_reset/done/$", auth_views.PasswordResetDoneView.as_view(
            template_name="myuser/password_reset_done.html",
            extra_context = {
                "phone_formatted": contactinfo(None)["phone_formatted"],
                "contact_email": contactinfo(None)["contactinfo"].contact_email,
            },
        ), name="site_password_reset_done"
    ),
    url(r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="myuser/password_reset_confirm.html",
            success_url = reverse_lazy("site_password_reset_complete")
        ), name="site_password_reset_confirm"
    ),
    url(r"^reset/done/$", auth_views.PasswordResetCompleteView.as_view(
        template_name="myuser/password_reset_complete.html"
        ), name="site_password_reset_complete"
    ),

    url(r"^signup/$", signup, name="signup"),
    url(r"^update/$", update_blogger, name="update_blogger"),
    url(r"^profile/$", show_blogger, name="show_blogger"),
    url(r"^new_affiliation/$", new_affiliation, name="new_affiliation"),
    url(r"^update_affiliation/$", update_affiliation, name="update_affiliation"),
    url(r"^affiliation/$", show_affiliation, name="show_affiliation"),
    url(r"^activation_sent/$", activation_sent, name="activation_sent"),
    url(r"^email_validated/$", email_validated, name="email_validated"),
    url(r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        activate, name="activate"),
]
