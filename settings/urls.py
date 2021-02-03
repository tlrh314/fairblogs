import filebrowser.sites
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.myuser.views import all_bloggers

handler403 = "pages.views.permission_denied"
handler404 = "pages.views.page_not_found"
handler500 = "pages.views.handler500"

urlpatterns = [
    path("admin/filebrowser/", filebrowser.sites.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path("admin/", include("django.contrib.auth.urls")),
    path("accounts/", include("apps.myuser.urls")),
    path("bloggers/", all_bloggers, name="all_bloggers"),
    path("", include("apps.blog.urls")),
    path("", include("apps.pages.urls")),
    path("search/", include("apps.search.urls")),
    path("captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
