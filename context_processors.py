from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

from blog.models import Post, Tag
from pages.models import ContactInfo


class ContactInfoDefault(object):
    def __init__(self):
        self.contact_email = settings.DEFAULT_FROM_EMAIL
        self.webmaster_email = settings.DEFAULT_FROM_EMAIL
        self.address = "Oetewalerstraat 83"
        self.postbox = "Amsterdam, 1093 ME"
        self.phone = "0031683210121"


def contactinfo(request):
    try:
        contactinfo = ContactInfo.objects.all()
        if contactinfo:
            contactinfo = contactinfo[0]
            p = contactinfo.phone
        else:
            contactinfo = ContactInfoDefault()
            p = contactinfo.phone
    except (OperationalError, ProgrammingError):
        print("Database was not yet created. Make migrations and migrate first.")
        contactinfo = ContactInfoDefault()
        p = contactinfo.phone

    phone_formatted = (
        "+" + p[2:4] + " (0)" + p[4:6] + " " + p[6:9] + " " + p[9:11] + " " + p[11:13]
    )

    return {"contactinfo": contactinfo, "phone_formatted": phone_formatted}


def base(request):
    """
    View that is inherited everywhere (for base template)
    """
    all_posts = Post.objects.all()
    popular_posts = all_posts.order_by("-popularity", "-date_created")
    if len(all_posts) >= 6:
        popular_posts = popular_posts[:7]

    return {"tags": Tag.objects.all(), "popular_posts": popular_posts}
