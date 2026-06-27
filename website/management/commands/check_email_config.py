import os

from django.conf import settings
from django.core.management.base import BaseCommand

from website.email_delivery import email_transport_label, resend_api_enabled, smtp_configured


class Command(BaseCommand):
    help = "Print email configuration diagnostics (for Railway Console)"

    def handle(self, *args, **options):
        env_key = os.environ.get("RESEND_API_KEY", "").strip()
        settings_key = getattr(settings, "RESEND_API_KEY", "").strip()

        self.stdout.write(f"Transport: {email_transport_label()}")
        self.stdout.write(f"RESEND_API_KEY in env: {'yes' if env_key else 'NO'}")
        self.stdout.write(f"RESEND_API_KEY in settings: {'yes' if settings_key else 'NO'}")
        self.stdout.write(f"EMAIL_PROVIDER: {os.environ.get('EMAIL_PROVIDER', '(not set)')}")
        self.stdout.write(f"EMAIL_HOST: {os.environ.get('EMAIL_HOST', '(not set)') or '(empty)'}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"Resend API active: {resend_api_enabled()}")
        self.stdout.write(f"SMTP configured: {smtp_configured()}")

        try:
            import resend  # noqa: F401

            self.stdout.write("resend package: installed")
        except ImportError:
            self.stdout.write(self.style.ERROR("resend package: NOT INSTALLED — push latest code and redeploy"))

        if resend_api_enabled():
            self.stdout.write(self.style.SUCCESS("Email ready via Resend HTTP API"))
        elif smtp_configured():
            self.stdout.write(self.style.WARNING("Using SMTP (may timeout on Railway)"))
        else:
            self.stdout.write(
                self.style.ERROR("Email NOT configured — set RESEND_API_KEY on Railway web service")
            )
