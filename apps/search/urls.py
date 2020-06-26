from __future__ import unicode_literals, absolute_import, division

from django.urls import path

from search.views import search


app_name = "search"
urlpatterns = [
    path("", view=search, name="terms"),
]
