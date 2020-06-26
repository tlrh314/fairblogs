import sys

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

import filebrowser.sites

from apps.myuser.views import all_bloggers


handler403 = "pages.views.permission_denied"
handler404 = "pages.views.page_not_found"
handler500 = "pages.views.handler500"

urlpatterns = [
    path(r"admin/filebrowser/", filebrowser.sites.site.urls),
    path(r"tinymce/", include("tinymce.urls")),
    path(r"admin/", admin.site.urls),
    path(r"admin/password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path(r"admin/", include("django.contrib.auth.urls")),
    path(r"accounts/", include("apps.myuser.urls")),
    path(r"bloggers/", all_bloggers, name="all_bloggers"),
    path(r"", include("apps.blog.urls")),
    path(r"", include("apps.pages.urls")),
    path(r"search/", include("apps.search.urls")),
    path(r"feeds/posts", include("apps.blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
