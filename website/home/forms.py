from django import forms
from django.core.validators import RegexValidator

from .models import Subscribers


class SubscibersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email', ]


phone_validator = RegexValidator(
    r'^\+?[0-9][0-9\s\-().]{6,18}$',
    'Enter a valid phone number, e.g. +91 97025 73082.',
)


class ContactForm(forms.Form):
    """Validates every contact / enquiry form on the site.

    The email field is called ``mail`` because that is what the existing
    templates post.
    """
    name = forms.CharField(min_length=2, max_length=255)
    mail = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=20, validators=[phone_validator])
    subject = forms.CharField(min_length=2, max_length=255)
    message = forms.CharField(max_length=5000, widget=forms.Textarea, required=False)
    # Ad attribution (utm_* / gclid) captured by JS on landing pages.
    tracking = forms.CharField(max_length=500, required=False)
    # Honeypot: hidden from people, filled in by bots.
    website = forms.CharField(required=False)

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Spam detected.')
        return ''
