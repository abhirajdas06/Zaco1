from django.conf import settings


def site_contact(request):
    """Site-wide contact details and switches, available to every template."""
    return {
        'CONTACT_PHONE': settings.CONTACT_PHONE_DISPLAY,
        'CONTACT_PHONE_TEL': settings.CONTACT_PHONE_TEL,
        'CONTACT_WHATSAPP': settings.CONTACT_WHATSAPP,
        'CONTACT_PHONE_2': settings.CONTACT_PHONE_2_DISPLAY,
        'CONTACT_PHONE_2_TEL': settings.CONTACT_PHONE_2_TEL,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
        'TRACKING_ENABLED': settings.TRACKING_ENABLED,
    }
