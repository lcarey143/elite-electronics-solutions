import uuid

from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.template.loader import render_to_string

from .models import Booking, Certification, Partner, PricingExtra, PricingPackage, Service, SiteSettings


def _mail_connection():
    timeout = getattr(settings, "EMAIL_TIMEOUT", 5)
    return get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        timeout=timeout,
    )


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
    mail_conn = _mail_connection()
    sent_count += send_mail(
        subject=admin_subject,
        message=admin_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings_obj.contact_email],
        fail_silently=True,
        connection=mail_conn,
    )
    sent_count += send_mail(
        subject=customer_subject,
        message=customer_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.email],
        fail_silently=True,
        connection=mail_conn,
    )
    mail_conn.close()
    return sent_count > 0


def build_ai_system_prompt():
    site = SiteSettings.load()
    services = Service.objects.filter(is_active=True)
    packages = PricingPackage.objects.filter(is_active=True)
    extras = PricingExtra.objects.filter(is_active=True)
    partners = Partner.objects.filter(is_active=True)
    certifications = Certification.objects.filter(is_active=True)

    lines = [
        f"You are the AI assistant for {site.company_name}, a systems integrator in {site.address_city}, {site.address_country}.",
        "Answer questions helpfully, professionally, and concisely about the company's services, pricing, booking, location, and partners.",
        "If you don't know something specific, suggest booking a free site visit or contacting the company directly.",
        "",
        f"Contact: {site.contact_email} | {site.contact_phone}",
        f"Address: {site.address_line1}, {site.address_line2}, {site.address_city}",
        f"Hours: {site.hours_weekday}; {site.hours_saturday}; {site.hours_sunday}",
        "",
        "SERVICES:",
    ]

    for svc in services:
        features = ", ".join(svc.features) if svc.features else ""
        lines.append(f"- {svc.title}: {svc.description} Features: {features}")

    lines.append("")
    lines.append("PRICING PACKAGES:")
    for pkg in packages:
        feature_list = "; ".join(pkg.features) if pkg.features else ""
        lines.append(f"- {pkg.tier_name}: from ${pkg.price}{pkg.price_suffix}. {feature_list}")

    lines.append("")
    lines.append("À LA CARTE:")
    for extra in extras:
        lines.append(f"- {extra.name}: {extra.price_label}")

    lines.append("")
    lines.append("PARTNERS & AUTHORIZED PRODUCTS:")
    for partner in partners:
        type_label = partner.get_partner_type_display()
        lines.append(f"- {partner.name} ({type_label}): {partner.description}")

    lines.append("")
    lines.append("CREDENTIALS & CERTIFICATIONS:")
    for cert in certifications:
        validity = f" Valid: {cert.valid_until}." if cert.valid_until else ""
        issuer = f" ({cert.issuer})" if cert.issuer else ""
        lines.append(f"- {cert.name}{issuer}: {cert.description}{validity}")

    lines.append("")
    lines.append(
        "To book a site visit, customers can use the booking form on the website. "
        "The team confirms within 24 hours and performs a free on-site assessment."
    )

    if site.ai_system_prompt_extra.strip():
        lines.append("")
        lines.append(site.ai_system_prompt_extra.strip())

    return "\n".join(lines)
