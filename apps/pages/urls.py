from django.urls import path

from pages.views import (
    about,
    contact,
    contact_success,
    disclaimer,
    page_not_found,
    permission_denied,
    privacy_policy,
)

app_name = "pages"
urlpatterns = [
    path(r"404.html", page_not_found, name="page_not_found"),
    path(r"denied/", permission_denied, name="permission_denied"),
    path(r"about/", about, name="about"),
    path(r"contact/", contact, name="contact"),
    path(r"thanks/", contact_success, name="contact_success"),
    path(r"privacy/", privacy_policy, name="privacy_policy"),
    path(r"disclaimer/", disclaimer, name="disclaimer"),
]
