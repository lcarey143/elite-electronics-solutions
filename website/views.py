import json
import logging
import os
import threading

from django.conf import settings
from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .forms import BookingForm
from .models import (
    AboutCard,
    Booking,
    Certification,
    FAQ,
    PricingExtra,
    PricingPackage,
    Project,
    Service,
    ServiceOption,
    Testimonial,
    Video,
)
from .services import build_ai_system_prompt, generate_booking_reference, send_booking_notification

logger = logging.getLogger(__name__)


def _send_booking_email_background(booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        sent = send_booking_notification(booking)
        logger.info("Background email for booking %s: sent=%s", booking.reference, sent)
    except Exception:
        logger.exception("Background email failed for booking id %s", booking_id)


@ensure_csrf_cookie
def home(request):
    return render(
        request,
        "website/home.html",
        {
            "services": Service.objects.filter(is_active=True)[:4],
        },
    )


@ensure_csrf_cookie
def about(request):
    return render(
        request,
        "website/pages/about.html",
        {
            "about_cards": AboutCard.objects.all(),
            "certifications": Certification.objects.filter(is_active=True),
        },
    )


@ensure_csrf_cookie
def services(request):
    return render(
        request,
        "website/pages/services.html",
        {"services": Service.objects.filter(is_active=True)},
    )


@ensure_csrf_cookie
def projects(request):
    return render(
        request,
        "website/pages/projects.html",
        {
            "projects": Project.objects.filter(is_active=True),
            "videos": Video.objects.filter(is_active=True, page="projects"),
        },
    )


@ensure_csrf_cookie
def pricing(request):
    return render(
        request,
        "website/pages/pricing.html",
        {
            "pricing_packages": PricingPackage.objects.filter(is_active=True),
            "pricing_extras": PricingExtra.objects.filter(is_active=True),
        },
    )


@ensure_csrf_cookie
def reviews(request):
    return render(
        request,
        "website/pages/reviews.html",
        {"testimonials": Testimonial.objects.filter(is_active=True)},
    )


@ensure_csrf_cookie
def faq(request):
    return render(
        request,
        "website/pages/faq.html",
        {"faqs": FAQ.objects.filter(is_active=True)},
    )


@ensure_csrf_cookie
def book(request):
    return render(
        request,
        "website/pages/book.html",
        {"service_options": ServiceOption.objects.filter(is_active=True)},
    )


@ensure_csrf_cookie
def contact(request):
    return render(request, "website/pages/contact.html")


@require_POST
@csrf_protect
def submit_booking(request):
    form = BookingForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    try:
        booking = form.save(commit=False)
        booking.services = list(form.cleaned_data.get("services", []))
        booking.reference = generate_booking_reference()
        booking.save()

        transaction.on_commit(
            lambda pk=booking.pk: threading.Thread(
                target=_send_booking_email_background,
                args=(pk,),
                daemon=True,
            ).start()
        )

        logger.info(
            "Booking saved: %s for %s (db=%s)",
            booking.reference,
            booking.email,
            connection.vendor,
        )

        return JsonResponse(
            {
                "success": True,
                "reference": booking.reference,
                "email_sent": False,
                "message": "Booking request received! Our team will contact you within 24 hours.",
            }
        )
    except Exception:
        logger.exception("Booking submission failed")
        return JsonResponse(
            {
                "success": False,
                "error": "Could not save your booking. Please call us at (242) 375-4179 or email lashardcarey@gmail.com.",
            },
            status=500,
        )


@require_POST
@csrf_protect
def ai_chat(request):
    if not settings.OPENAI_API_KEY:
        return JsonResponse(
            {
                "success": False,
                "error": "AI assistant is not configured yet. Please add OPENAI_API_KEY.",
            },
            status=503,
        )

    try:
        body = json.loads(request.body)
        message = body.get("message", "").strip()
        history = body.get("history", [])
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid request."}, status=400)

    if not message:
        return JsonResponse({"success": False, "error": "Message is required."}, status=400)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        messages = [{"role": "system", "content": build_ai_system_prompt()}]

        for item in history[-8:]:
            role = item.get("role")
            content = item.get("content", "").strip()
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=600,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        return JsonResponse({"success": True, "reply": reply})
    except Exception as exc:
        return JsonResponse(
            {"success": False, "error": f"AI service error: {exc}"},
            status=500,
        )


@require_GET
def health_check(request):
    """Always return 200 so Railway healthchecks pass once gunicorn is up."""
    payload = {"status": "ok"}
    try:
        ServiceOption.objects.exists()
        payload["database"] = "ok"
        payload["engine"] = settings.DATABASES["default"]["ENGINE"].split(".")[-1]
        payload["bookings"] = Booking.objects.count()
        if os.environ.get("RAILWAY_ENVIRONMENT") and payload["engine"] == "sqlite3":
            payload["warning"] = "Add PostgreSQL on Railway — SQLite data is not persistent"
    except Exception as exc:
        payload["database"] = "error"
        payload["database_error"] = str(exc)
        logger.warning("Health DB check failed: %s", exc)
    return JsonResponse(payload)
