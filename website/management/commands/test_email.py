import os

from django.conf import settings
from django.core.management.base import BaseCommand

from website.email_delivery import email_transport_label, resend_api_enabled, send_text_email, smtp_configured


class Command(BaseCommand):
    help = "Send a test email to verify email configuration (Resend API or SMTP)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            default=None,
            help="Recipient email (defaults to SiteSettings contact email)",
        )

    def handle(self, *args, **options):
        from website.models import SiteSettings

        site = SiteSettings.load()
        recipient = options.get("to") or site.contact_email

        if not resend_api_enabled() and not smtp_configured():
            self.stdout.write(self.style.ERROR("Email not configured."))
            self.stdout.write(
                "Diagnostics: "
                f"EMAIL_PROVIDER={os.environ.get('EMAIL_PROVIDER', '(not set)')!r}, "
                f"RESEND_API_KEY={'set' if os.environ.get('RESEND_API_KEY', '').strip() else 'NOT SET'}, "
                f"EMAIL_HOST={os.environ.get('EMAIL_HOST', '(not set)')!r}"
            )
            self.stdout.write("On Railway: set RESEND_API_KEY=re_... (HTTP API, no SMTP needed).")
            return

        self.stdout.write(f"Transport: {email_transport_label()}")
        self.stdout.write(f"From: {settings.DEFAULT_FROM_EMAIL}")

        try:
            send_text_email(
                subject=f"EES Test Email — {site.company_name}",
                body=(
                    "This is a test email from your Elite Electronics Solutions website.\n\n"
                    "If you received this, booking notification emails are configured correctly."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient,
            )
            self.stdout.write(self.style.SUCCESS(f"Test email sent to {recipient}"))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Email failed: {exc}"))
