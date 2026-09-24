from django.conf import settings


def site_contact(request):
    """Make the site-wide phone/WhatsApp details available to every template."""
    return {
        'CONTACT_PHONE': settings.CONTACT_PHONE_DISPLAY,
        'CONTACT_PHONE_TEL': settings.CONTACT_PHONE_TEL,
        'CONTACT_WHATSAPP': settings.CONTACT_WHATSAPP,
    }
