from __future__ import unicode_literals, absolute_import, division

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from context_processors import contactinfo
from myuser.views import signup
from myuser.views import new_affiliation
from myuser.views import set_affiliation
from myuser.views import activation_sent
from myuser.views import activate
from myuser.views import email_validated
from myuser.views import update_blogger
from myuser.views import show_blogger
from myuser.views import update_affiliation
from myuser.views import show_affiliation


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(
        template_name="myuser/login.html"
        ), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(
        template_name="myuser/logged_out.html"
        ), name="logout"
    ),

    path("password_change/", auth_views.PasswordChangeView.as_view(
        template_name="myuser/password_change_form.html",
        success_url = reverse_lazy("site_password_change_done")
        ), name="site_password_change"
    ),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="myuser/password_change_done.html",
        ), name="site_password_change_done"
    ),
    path("password_reset/", auth_views.PasswordResetView.as_view(
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
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
            template_name="myuser/password_reset_done.html",
            extra_context = {
                "phone_formatted": contactinfo(None)["phone_formatted"],
                "contact_email": contactinfo(None)["contactinfo"].contact_email,
            },
        ), name="site_password_reset_done"
    ),
    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="myuser/password_reset_confirm.html",
            success_url = reverse_lazy("site_password_reset_complete")
        ), name="site_password_reset_confirm"
    ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="myuser/password_reset_complete.html"
        ), name="site_password_reset_complete"
    ),

    path("signup/", signup, name="signup"),
    path("update/", update_blogger, name="update_blogger"),
    path("profile/", show_blogger, name="show_blogger"),
    path("new_affiliation/", new_affiliation, name="new_affiliation"),
    path("set_affiliation/", set_affiliation, name="set_affiliation"),
    path("update_affiliation/", update_affiliation, name="update_affiliation"),
    path("affiliation/", show_affiliation, name="show_affiliation"),
    path("activation_sent/", activation_sent, name="activation_sent"),
    path("email_validated/", email_validated, name="email_validated"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
