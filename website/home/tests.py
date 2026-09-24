import django
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Contact, Subscribers

RECIPIENTS = ['info@zacoinfotech.com', 'abhiraj@zacocomputer.com']

# Tests run with DEBUG off, so switch off the HTTPS redirect and the
# manifest-based static storage (needs collectstatic) for the test client.
_plain_static = 'django.contrib.staticfiles.storage.StaticFilesStorage'
if django.VERSION >= (4, 2):
    _storage = {'STORAGES': {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': _plain_static},
    }}
else:
    _storage = {'STATICFILES_STORAGE': _plain_static}

test_settings = override_settings(
    SECURE_SSL_REDIRECT=False,
    LEAD_NOTIFICATION_EMAILS=RECIPIENTS,
    **_storage,
)

VALID = {
    'name': 'Asha Rao',
    'mail': 'asha@example.com',
    'phone': '+91 98765 43210',
    'subject': 'Web Development - Custom Website',
    'message': 'Need a website for my clinic.',
}


@test_settings
class ContactFormTests(TestCase):
    def test_valid_submission_saves_and_emails_both_recipients(self):
        r = self.client.post(reverse('contact'), {**VALID, 'next': '/services/web-development#enquiry'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['Location'], '/services/web-development#enquiry')
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, RECIPIENTS)
        self.assertEqual(msg.reply_to, ['asha@example.com'])
        self.assertIn('+91 98765 43210', msg.body)
        self.assertIn('Need a website for my clinic.', msg.body)

    def test_success_message_is_tagged_as_lead_for_conversion_tracking(self):
        r = self.client.post(reverse('contact'), VALID, follow=True)
        tags = [m.tags for m in r.context['messages']]
        self.assertTrue(any('lead' in t and 'success' in t for t in tags))

    def test_message_is_optional_for_landing_page_form(self):
        data = {**VALID, 'message': '', 'tracking': 'utm_source=google&gclid=abc'}
        self.client.post(reverse('contact'), data)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertIn('utm_source=google&gclid=abc', mail.outbox[0].body)

    def test_invalid_submission_does_not_crash_or_send(self):
        # This used to return None from the view -> HTTP 500.
        r = self.client.post(reverse('contact'), {**VALID, 'mail': 'not-an-email'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(any('danger' in m.tags for m in r.context['messages']))

    def test_missing_fields_do_not_crash(self):
        r = self.client.post(reverse('contact'), {})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Contact.objects.count(), 0)

    def test_honeypot_is_silently_dropped(self):
        r = self.client.post(reverse('contact'), {**VALID, 'website': 'http://spam.example'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_smtp_failure_still_saves_lead_and_thanks_visitor(self):
        with override_settings(EMAIL_BACKEND='home.tests.BrokenBackend'):
            r = self.client.post(reverse('contact'), VALID, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)

    def test_redirect_target_cannot_leave_the_site(self):
        r = self.client.post(reverse('contact'), {**VALID, 'next': 'https://evil.example/'})
        self.assertEqual(r['Location'], '/contact')

    def test_phone_up_to_20_chars_is_stored(self):
        self.client.post(reverse('contact'), {**VALID, 'phone': '+91 97025 73082'})
        self.assertEqual(Contact.objects.get().phone, '+91 97025 73082')


class BrokenBackend:
    def __init__(self, *a, **k):
        pass

    def send_messages(self, messages):
        raise OSError('SMTP down')


@test_settings
class NewsletterTests(TestCase):
    def test_subscribe_saves_notifies_and_dedupes(self):
        url = reverse('subscribe')
        self.client.post(url, {'email': 'reader@example.com', 'next': '/about'})
        self.client.post(url, {'email': 'reader@example.com', 'next': '/about'})
        self.assertEqual(Subscribers.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, RECIPIENTS)

    def test_invalid_email_rejected(self):
        r = self.client.post(reverse('subscribe'), {'email': 'nope'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Subscribers.objects.count(), 0)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(reverse('subscribe')).status_code, 405)


@test_settings
class PageTests(TestCase):
    PAGES = [
        '/', '/about', '/contact', '/services/', '/services/web-development',
        '/services/application-development', '/services/digital-marketing',
        '/services/ui-ux', '/services/custom-software',
        '/services/technical-consultation', '/hosting', '/shared_hosting',
        '/web_hosting', '/web_hosting_plus', '/technologies',
        '/technologies/frontend', '/technologies/backend',
        '/technologies/database', '/faq', '/terms-and-conditions', '/blog/',
    ] + [
        f'/{c}/{p}' for c in ('canada', 'usa', 'uk') for p in (
            '', 'about/', 'services/', 'website_development/', 'seo/', 'smm/',
            'custom_software/', 'digital_marketing/', 'technical-consultancy/',
            'contact/',
        )
    ]
    OLD_NUMBERS = ['69288800', '9288 800', '7710051543', '587 435 3187',
                   '7785 246 591', '98765 43210']

    def test_every_page_renders_with_new_number_only(self):
        for url in self.PAGES:
            with self.subTest(url=url):
                r = self.client.get(url)
                self.assertEqual(r.status_code, 200)
                body = r.content.decode()
                for old in self.OLD_NUMBERS:
                    self.assertNotIn(old, body)

    def test_new_number_present_in_header_and_tel_links(self):
        body = self.client.get('/').content.decode()
        self.assertIn('+91 97025 73082', body)
        self.assertIn('tel:+919702573082', body)

    def test_country_contact_forms_post_to_real_endpoint(self):
        for url in ['/canada/contact/', '/usa/contact/', '/uk/contact/']:
            with self.subTest(url=url):
                body = self.client.get(url).content.decode()
                self.assertIn('action="/contact"', body)
                self.assertIn(f'name="next" value="{url}"', body)

    def test_web_development_landing_page_ctas(self):
        body = self.client.get('/services/web-development').content.decode()
        self.assertIn('href="#enquiry"', body)
        self.assertIn('tel:+919702573082', body)
        self.assertIn('wa.me/919702573082', body)
        self.assertIn('id="zc-lead-form"', body)
        self.assertIn('action="/contact"', body)
        self.assertIn('zc-sticky', body)

    def test_flash_message_is_rendered_visibly(self):
        r = self.client.post('/subscribe', {'email': 'x@example.com', 'next': '/about'}, follow=True)
        body = r.content.decode()
        self.assertIn('site-flash', body)
        self.assertIn('Subscription Successful', body)


@test_settings
class LandingPageConversionTests(TestCase):
    def test_conversion_events_fire_after_successful_lead(self):
        r = self.client.post(reverse('contact'), {**VALID, 'next': '/services/web-development#enquiry'}, follow=True)
        body = r.content.decode()
        self.assertIn("gtag('event', 'generate_lead'", body)
        self.assertIn("fbq('track', 'Lead')", body)
        self.assertIn('Thank you for your submission', body)

    def test_no_conversion_event_on_plain_page_view(self):
        body = self.client.get('/services/web-development').content.decode()
        self.assertNotIn("gtag('event', 'generate_lead'", body)


class ForgivingStorageTests(TestCase):
    """The theme CSS references files that were never shipped; deploys must survive that."""

    def test_missing_css_reference_does_not_break_collectstatic_hashing(self):
        import tempfile
        from pathlib import Path
        from django.core.files.base import ContentFile
        from website.storage import ForgivingManifestStaticFilesStorage

        with tempfile.TemporaryDirectory() as root:
            storage = ForgivingManifestStaticFilesStorage(location=root, base_url='/static/')
            storage.save('a/ok.png', ContentFile(b'png'))
            storage.save('a/site.css', ContentFile(
                b'.a{background:url(ok.png)} .b{background:url(missing.eot)}'))
            paths = {'a/ok.png': (storage, 'a/ok.png'), 'a/site.css': (storage, 'a/site.css')}
            results = list(storage.post_process(paths, dry_run=False))
            errors = [r for r in results if isinstance(r[2], Exception)]
            self.assertEqual(errors, [])
            # existing file gets a hashed name, missing one is left alone
            css = [p for p in Path(root).rglob('site.*.css')][0].read_text()
            self.assertRegex(css, r'ok\.[0-9a-f]{12}\.png')
            self.assertIn('missing.eot', css)
            # and a template-style lookup of a missing file no longer raises
            self.assertEqual(storage.url('nope/missing.png'), '/static/nope/missing.png')


@test_settings
class ServicePagesCtaTests(TestCase):
    """Every service page shares the same CTA structure (hero, form, sticky bar)."""

    PAGES = {
        '/services/': 'Services - Web Development',
        '/services/web-development': 'Web Development - Custom Website',
        '/services/application-development': 'App Development - Android App',
        '/services/digital-marketing': 'Digital Marketing - SEO',
        '/services/ui-ux': 'UI/UX - Website Design',
        '/services/custom-software': 'Custom Software - Business Software',
        '/services/technical-consultation': 'Technical Consulting - Technology Strategy',
    }

    def test_each_page_has_full_cta_structure(self):
        for url, first_option in self.PAGES.items():
            with self.subTest(url=url):
                body = self.client.get(url).content.decode()
                self.assertEqual(body.count('class="zc-hero-cta"'), 1)
                self.assertEqual(body.count('id="enquiry"'), 1)
                self.assertEqual(body.count('id="zc-lead-form"'), 1)
                self.assertEqual(body.count('class="zc-sticky"'), 1)
                self.assertIn('href="#enquiry"', body)
                self.assertIn('tel:+919702573082', body)
                self.assertIn('wa.me/919702573082?text=Hi%20Zaco%2C%20I%27m%20interested%20in%20', body)
                self.assertIn('action="/contact"', body)
                self.assertIn(f'value="{first_option}"', body)
                self.assertIn(f'name="next" value="{url}#enquiry"', body)
                self.assertIn('Get a Free Quote', body)
                # old CTA-less hero button is gone
                self.assertNotIn('dia-banner-btn', body.split('zc-hero-cta')[0][-400:])

    def test_each_page_has_unique_title_and_description(self):
        titles = set()
        for url in self.PAGES:
            body = self.client.get(url).content.decode()
            self.assertIn('Get a Free Quote - Zaco</title>', body, url)
            self.assertIn('+91 97025 73082', body.split('name="description"')[1][:250], url)
            titles.add(body.split('<title>')[1].split('</title>')[0])
        self.assertEqual(len(titles), len(self.PAGES))

    def test_lead_from_each_page_is_emailed_with_page_subject(self):
        for url, option in self.PAGES.items():
            with self.subTest(url=url):
                mail.outbox.clear()
                r = self.client.post(reverse('contact'), {
                    **VALID, 'subject': option, 'next': f'{url}#enquiry'}, follow=True)
                self.assertEqual(r.status_code, 200)
                self.assertEqual(mail.outbox[0].to, RECIPIENTS)
                self.assertIn(option, mail.outbox[0].subject)
                self.assertIn("gtag('event', 'generate_lead'", r.content.decode())
