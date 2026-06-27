from django.contrib import admin

from .models import (
    AboutCard,
    Booking,
    Certification,
    Partner,
    PricingExtra,
    PricingPackage,
    Service,
    ServiceOption,
    SiteSettings,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Company", {"fields": ("company_name", "tagline", "hero_subtitle", "pricing_note")}),
        ("Contact", {"fields": ("contact_email", "contact_phone")}),
        (
            "Address",
            {"fields": ("address_line1", "address_line2", "address_city", "address_country", "maps_query")},
        ),
        ("Hours", {"fields": ("hours_weekday", "hours_saturday", "hours_sunday")}),
        ("AI Assistant", {"fields": ("ai_system_prompt_extra",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutCard)
class AboutCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


@admin.register(PricingPackage)
class PricingPackageAdmin(admin.ModelAdmin):
    list_display = ("tier_name", "price", "is_featured", "order", "is_active")
    list_editable = ("price", "is_featured", "order", "is_active")
    list_filter = ("is_active", "is_featured")


@admin.register(PricingExtra)
class PricingExtraAdmin(admin.ModelAdmin):
    list_display = ("name", "price_label", "order", "is_active")
    list_editable = ("price_label", "order", "is_active")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation", "partner_type", "order", "is_active")
    list_editable = ("order", "is_active", "partner_type")
    list_filter = ("is_active", "partner_type")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "issuer", "category", "valid_until", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "category")


@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference", "full_name", "email", "preferred_date", "status", "created_at")
    list_filter = ("status", "property_type", "preferred_date")
    search_fields = ("reference", "full_name", "email", "phone")
    readonly_fields = ("reference", "created_at")
    list_editable = ("status",)
