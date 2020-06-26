from __future__ import unicode_literals, absolute_import, division

from django.urls import path, include, reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from pages.views import about
from pages.views import contact
from pages.views import contact_success
from pages.views import privacy_policy
from pages.views import disclaimer
from pages.views import page_not_found
from pages.views import permission_denied


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
