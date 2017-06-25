"""fairblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import sys

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
import django.views.static

import filebrowser.sites
from ajax_select import urls as ajax_select_urls

# TODO: set handler404/500
# handler404 = "main.views.page_not_found"
# handler500 = "main.views.page_not_found"

urlpatterns = [
    url(r'^admin/filebrowser/', include(filebrowser.sites.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'', include('apps.blog.urls')),
    url(r'', include('apps.pages.urls')),
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

