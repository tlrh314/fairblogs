# Note that in order to import from django we first need to load all settings
# from the per-domain setup, so the parameters below are imported there

# http://django-filebrowser.readthedocs.io/en/latest/settings.html
# Filebrowser only eats from settings, not from local_settings
# FILEBROWSER_DIRECTORY = "/media/uploads"
FILEBROWSER_DEFAULT_PERMISSIONS = 0o644
FILEBROWSER_EXTENSIONS = {
    "Image": [".jpg", ".jpeg", ".gif", ".png", ".tif", ".tiff"],
    "Document": [], # [".pdf", ".doc", ".rtf", ".txt", ".xls", ".csv"],
    "Video": [], # [".mov", ".wmv", ".mpeg", ".mpg", ".avi", ".rm"],
    "Audio": [], # [".mp3", ".mp4", ".wav", ".aiff", ".midi", ".m4p"]
}
FILEBROWSER_ADMIN_VERSIONS = ["big"]  # "thumbnail", "small", "medium", "large"

from django.core.files.storage import FileSystemStorage
from filebrowser.sites import site
from django.conf import settings
site.storage = FileSystemStorage(location=settings.STATIC_ROOT, base_url="/static/")
site.directory = "img/"

# For files uploaded via submit form
FILE_UPLOAD_PERMISSIONS = 0o644
