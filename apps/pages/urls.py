from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import include, url
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import about
from .views import contact
from .views import contact_success
from .views import privacy_policy
from .views import disclaimer
from .views import page_not_found


urlpatterns = [
    url(r"^404.html$", page_not_found, name="page_not_found"),
    url(r"^about/$", about, name="about"),
    url(r"^contact/$", contact, name="contact"),
    url(r"^thanks/$", contact_success, name="contact_success"),
    url(r"^privacy/$", privacy_policy, name="privacy_policy"),
    url(r"^disclaimer/$", disclaimer, name="disclaimer"),

]
