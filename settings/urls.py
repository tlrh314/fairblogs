"""fairblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""

import sys

import django.views.static
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include, url, handler404, handler500
from django.contrib.auth import views as auth_views

import filebrowser.sites
from ajax_select import urls as ajax_select_urls

from apps.myuser.views import all_bloggers


handler404 = "apps.pages.views.page_not_found"
handler500 = "apps.pages.views.page_not_found"

urlpatterns = [
    url(r"^admin/filebrowser/", include(filebrowser.sites.site.urls)),
    url(r"^tinymce/", include("tinymce.urls")),
    url(r"^ajax_select/", include(ajax_select_urls)),
    url(r"^admin/", admin.site.urls),
    url(r"^admin/password_reset/$", auth_views.PasswordResetView.as_view(), name="password_reset"),
    url(r'^admin/', include('django.contrib.auth.urls')),
    url(r"^accounts/", include("apps.myuser.urls")),
    url(r"^bloggers/", all_bloggers, name="all_bloggers"),
    url(r"", include("apps.blog.urls", namespace="blogs")),
    url(r"", include("apps.pages.urls", namespace="pages")),
    url(r"^search/", include("apps.search.urls", namespace="search")),
]

if "runserver" in sys.argv:
    urlpatterns += [
        url(r"^static/(?P<path>.*)$",
            django.views.static.serve,
            {"document_root": settings.STATIC_ROOT}),
        url(r"^media/(?P<path>.*)$",
            django.views.static.serve,
            {"document_root": settings.MEDIA_ROOT}),
        url(r"^(?P<path>robots.txt)$",
            django.views.static.serve,
            {"document_root": settings.MEDIA_ROOT}),
    ]

