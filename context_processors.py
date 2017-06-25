from __future__ import unicode_literals, absolute_import, division

from apps.pages.models import ContactInfo
from apps.blog.models import Tag

from django.db.utils import OperationalError


class ContactInfoDefault(object):
    def __init__(self):
        self.contact_email = "hello@fairblogs.nl"
        self.webmaster_email = "hello@fairblogs.nl"
        self.address = "Oetewalerstraat 83"
        self.postbox = "Amsterdam, 1093 ME"
        self.phone = "0031683210121"


def contactinfo(request):
    contactinfo = ContactInfo.objects.all()
    try:
        if contactinfo:
            contactinfo = contactinfo[0]
            p = contactinfo.phone
        else:
            contactinfo = ContactInfoDefault()
            p = contactinfo.phone
    except OperationalError as e:
        print("Database was not yet created. Make migrations and migrate first.")
        contactinfo = ContactInfoDefault()
        p = contactinfo.phone

    phone_formatted = "+"+p[2:4]+" (0)"+p[4:6]+" "+p[6:9]+" "+p[9:11]+" "+p[11:13]

    return {"contactinfo": contactinfo, "phone_formatted": phone_formatted }


def base(request):
    """
    View that is inherited everywhere (for base template)
    """
    return {"tags": Tag.objects.all()}
