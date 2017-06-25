from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import include, url
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from apiweb.context_processors import contactinfo
from .views import redirect_to_profile, page_not_found
from .views import index, contact, contact_success, privacy_policy
from .views import site_contactinfo, site_careerinfo, site_theses


urlpatterns = [
    url(r'^404.html$', page_not_found, name='page_not_found'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^thanks/$', contact_success, name='contact_success'),
    url(r'^privacy-policy/$', privacy_policy, name='privacy_policy'),
]
