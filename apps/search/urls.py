from __future__ import unicode_literals, absolute_import, division

from django.conf.urls import url

from .views import search


urlpatterns = [
    url(r"^$", view=search, name="terms"),
]
