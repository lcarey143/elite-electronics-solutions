import logging

from django.conf import settings
from django.core.mail import get_connection, send_mail

logger = logging.getLogger(__name__)


def resend_api_enabled() -> bool:
    key = getattr(settings, "RESEND_API_KEY", "").strip()
    if not key:
        import os

        key = os.environ.get("RESEND_API_KEY", "").strip()
    return bool(key)


def smtp_configured() -> bool:
    return bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)


def send_text_email(*, subject: str, body: str, from_email: str, to: str) -> bool:
    """Send a plain-text email via Resend HTTP API or SMTP."""
    if resend_api_enabled():
        return _send_via_resend(subject=subject, body=body, from_email=from_email, to=to)
    if smtp_configured():
        return _send_via_smtp(subject=subject, body=body, from_email=from_email, to=to)
    logger.warning("Email not configured: set RESEND_API_KEY or SMTP credentials")
    return False


def _send_via_resend(*, subject: str, body: str, from_email: str, to: str) -> bool:
    import os

    import resend

    api_key = getattr(settings, "RESEND_API_KEY", "").strip() or os.environ.get("RESEND_API_KEY", "").strip()
    resend.api_key = api_key
    resend.Emails.send(
        {
            "from": from_email,
            "to": [to],
            "subject": subject,
            "text": body,
        }
    )
    return True


def _send_via_smtp(*, subject: str, body: str, from_email: str, to: str) -> bool:
    timeout = getattr(settings, "EMAIL_TIMEOUT", 10)
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        timeout=timeout,
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to],
            fail_silently=False,
            connection=connection,
        )
        return True
    finally:
        connection.close()


def email_transport_label() -> str:
    if resend_api_enabled():
        return "Resend HTTP API"
    if smtp_configured():
        return f"SMTP {settings.EMAIL_HOST}:{settings.EMAIL_PORT}"
    return "not configured"
