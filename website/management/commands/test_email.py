from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Send a test email to verify Railway SMTP configuration"

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

        if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
            self.stdout.write(self.style.ERROR("EMAIL_BACKEND is console — set SMTP vars on Railway first."))
            return

        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(self.style.ERROR("EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not set."))
            return

        try:
            send_mail(
                subject=f"EES Test Email — {site.company_name}",
                message=(
                    "This is a test email from your Elite Electronics Solutions website.\n\n"
                    "If you received this, booking notification emails are configured correctly."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Test email sent to {recipient}"))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Email failed: {exc}"))
