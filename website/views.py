import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST

from .forms import BookingForm
from .models import (
    AboutCard,
    Certification,
    Partner,
    PricingExtra,
    PricingPackage,
    Service,
    ServiceOption,
    SiteSettings,
)
from .services import build_ai_system_prompt, generate_booking_reference, send_booking_notification


def home(request):
    site = SiteSettings.load()
    context = {
        "site": site,
        "about_cards": AboutCard.objects.all(),
        "services": Service.objects.filter(is_active=True),
        "pricing_packages": PricingPackage.objects.filter(is_active=True),
        "pricing_extras": PricingExtra.objects.filter(is_active=True),
        "partners": Partner.objects.filter(is_active=True),
        "certifications": Certification.objects.filter(is_active=True),
        "service_options": ServiceOption.objects.filter(is_active=True),
        "booking_form": BookingForm(),
    }
    return render(request, "website/home.html", context)


@require_POST
@csrf_protect
def submit_booking(request):
    form = BookingForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    booking = form.save(commit=False)
    booking.reference = generate_booking_reference()
    booking.save()

    try:
        send_booking_notification(booking)
        email_sent = True
    except Exception as exc:
        email_sent = False
        import logging
        logging.getLogger(__name__).warning("Booking email failed: %s", exc)

    return JsonResponse(
        {
            "success": True,
            "reference": booking.reference,
            "email_sent": email_sent,
            "message": "Booking request received! Our team will contact you within 24 hours.",
        }
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
    return JsonResponse({"status": "ok"})
