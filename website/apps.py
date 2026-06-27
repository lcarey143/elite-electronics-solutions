from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"

    def ready(self):
        import logging

        from django.conf import settings

        from .email_delivery import email_transport_label, resend_api_enabled

        logger = logging.getLogger("website")
        if resend_api_enabled():
            logger.info("Email: %s (from %s)", email_transport_label(), settings.DEFAULT_FROM_EMAIL)
        elif settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            logger.info("Email: SMTP %s:%s", settings.EMAIL_HOST, settings.EMAIL_PORT)
        else:
            logger.warning("Email: not configured — set RESEND_API_KEY on Railway")
