import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Booking, Certification, Partner, PricingExtra, PricingPackage, Service, SiteSettings


def generate_booking_reference():
    return f"EES-{uuid.uuid4().hex[:8].upper()}"


def send_booking_notification(booking: Booking):
    """Send admin + customer emails. Returns True if at least one email was sent."""
    if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
        return False

    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        return False

    settings_obj = SiteSettings.load()
    context = {
        "booking": booking,
        "property_type_display": booking.get_property_type_display(),
        "time_display": booking.get_preferred_time_display(),
    }

    admin_subject = f"New Site Visit Request — {booking.reference}"
    admin_body = render_to_string("website/emails/booking_admin.txt", context)

    customer_subject = f"Site Visit Request Received — {booking.reference}"
    customer_body = render_to_string("website/emails/booking_customer.txt", context)

    sent_count = 0
    sent_count += send_mail(
        subject=admin_subject,
        message=admin_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings_obj.contact_email],
        fail_silently=True,
    )
    sent_count += send_mail(
        subject=customer_subject,
        message=customer_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.email],
        fail_silently=True,
    )
    return sent_count > 0
