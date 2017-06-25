from __future__ import unicode_literals, absolute_import, division

from apps.pages.models import ContactInfo
from apps.blog.models import Tag


def contactinfo(request):
    contactinfo = ContactInfo.objects.all()
    if contactinfo:
        contactinfo = contactinfo[0]
        p = contactinfo.phone
    else:
        contactinfo = dict()
        # Hardcoded in case ContactInfo has no instances.
        contactinfo["contact_email"] = "hello@fairblogs.nl"
        contactinfo["webmaster_email"] = "hello@fairblogs.nl"
        contactinfo["address"] = "Oetewalerstraat 83"
        contactinfo["postbox"] = "Amsterdam, 1093 ME"
        contactinfo["phone"] = default="0031683210121"
        p = contactinfo.get("phone")

    phone_formatted = "+"+p[2:4]+" (0)"+p[4:6]+" "+p[6:9]+" "+p[9:11]+" "+p[11:13]

    return {"contactinfo": contactinfo, "phone_formatted": phone_formatted }


def base(request):
    """
    View that is inherited everywhere (for base template)
    """
    return {"tags": Tag.objects.all()}
