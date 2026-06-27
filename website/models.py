from django.db import models


class SiteSettings(models.Model):
    """Singleton site-wide settings editable from admin."""

    company_name = models.CharField(max_length=200, default="Elite Electronics Solutions")
    tagline = models.CharField(
        max_length=300,
        default="Systems Integrator · Freeport, Grand Bahama",
    )
    hero_subtitle = models.TextField(
        default=(
            "Security systems, life safety, CCTV, access control, fire alarms & communications — "
            "from residential installs to full commercial deployments."
        )
    )
    contact_email = models.EmailField(default="lashardcarey@gmail.com")
    contact_phone = models.CharField(max_length=30, default="(242) 375-4179")
    address_line1 = models.CharField(max_length=200, default="Unit #7 Millennium Mall")
    address_line2 = models.CharField(max_length=200, default="West Atlantic Drive")
    address_city = models.CharField(max_length=100, default="Freeport, Grand Bahama")
    address_country = models.CharField(max_length=100, default="The Bahamas")
    hours_weekday = models.CharField(max_length=100, default="Monday – Friday: 8:00 AM – 5:00 PM")
    hours_saturday = models.CharField(max_length=100, default="Saturday: 9:00 AM – 1:00 PM")
    hours_sunday = models.CharField(max_length=100, default="Sunday: Closed")
    maps_query = models.CharField(
        max_length=300,
        default="Millennium+Mall+West+Atlantic+Drive+Freeport+Grand+Bahama",
    )
    pricing_note = models.CharField(
        max_length=200,
        default="Starting estimates — final quotes provided after site assessment",
    )
    meta_description = models.TextField(
        default=(
            "Elite Electronics Solutions — CCTV, access control, fire alarms, SAFR facial recognition "
            "and full security integration in Freeport, Grand Bahama. Free site visits."
        ),
    )
    whatsapp_number = models.CharField(
        max_length=20,
        default="12423754179",
        help_text="Digits only for WhatsApp link, e.g. 12423754179",
    )
    google_reviews_url = models.URLField(
        blank=True,
        help_text="Link to your Google Business Profile reviews page",
    )
    trust_items = models.JSONField(
        default=list,
        help_text='Trust strip items, e.g. ["Free site visits", "Axis authorized partner"]',
    )
    stat_projects = models.CharField(max_length=40, default="100+", blank=True)
    stat_years = models.CharField(max_length=40, default="10+", blank=True)
    stat_support = models.CharField(max_length=40, default="Local team", blank=True)
    ai_system_prompt_extra = models.TextField(
        blank=True,
        help_text="Extra instructions for the AI assistant (optional).",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def phone_tel(self):
        digits = "".join(c for c in self.contact_phone if c.isdigit())
        if len(digits) == 10:
            return f"+1{digits}"
        if digits.startswith("1") and len(digits) == 11:
            return f"+{digits}"
        return f"+{digits}" if digits else self.contact_phone

    @property
    def whatsapp_url(self):
        digits = "".join(c for c in self.whatsapp_number if c.isdigit())
        return f"https://wa.me/{digits}" if digits else ""

    def get_trust_items(self):
        if self.trust_items:
            return self.trust_items
        return [
            "Free site visits & assessments",
            "Axis & SAFR authorized partner",
            "BICSI-certified professionals",
            "Local Grand Bahama team",
        ]


class AboutCard(models.Model):
    icon = models.CharField(max_length=10, default="🛡️")
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Service(models.Model):
    icon = models.CharField(max_length=10, default="📹")
    title = models.CharField(max_length=120)
    description = models.TextField()
    features = models.JSONField(default=list, help_text='List of feature strings, e.g. ["Indoor cameras", "NVR setup"]')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class PricingPackage(models.Model):
    tier_name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_suffix = models.CharField(max_length=10, default="+", help_text='e.g. "+" or "/mo"')
    price_note = models.CharField(max_length=80, default="Starting from")
    features = models.JSONField(default=list)
    is_featured = models.BooleanField(default=False)
    badge_text = models.CharField(max_length=40, blank=True, default="Most Popular")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.tier_name} — ${self.price}{self.price_suffix}"


class PricingExtra(models.Model):
    name = models.CharField(max_length=120)
    price_label = models.CharField(max_length=80, help_text='e.g. "From $150" or "Custom quote"')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Pricing extras"

    def __str__(self):
        return f"{self.name} — {self.price_label}"


class Partner(models.Model):
    PARTNER_TYPES = [
        ("reseller", "Reseller"),
        ("authorized", "Authorized Partner"),
        ("installer", "Authorized Installer"),
    ]

    abbreviation = models.CharField(max_length=10)
    name = models.CharField(max_length=120)
    description = models.TextField()
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES, default="reseller")
    logo = models.CharField(
        max_length=200,
        blank=True,
        help_text='Static asset path, e.g. "assets/partners/axis-authorized.png"',
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Certification(models.Model):
    CATEGORIES = [
        ("certification", "Professional Certification"),
        ("affiliation", "Industry Affiliation"),
        ("partner_badge", "Partner Badge"),
    ]

    name = models.CharField(max_length=160)
    issuer = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    image = models.CharField(
        max_length=200,
        help_text='Static asset path, e.g. "assets/certifications/bicsi-inst1.png"',
    )
    valid_until = models.CharField(
        max_length=80,
        blank=True,
        help_text='Optional validity text, e.g. "Oct 25, 2025 - Oct 25, 2029"',
    )
    category = models.CharField(max_length=20, choices=CATEGORIES, default="certification")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ServiceOption(models.Model):
    """Checkbox options shown on the booking form."""

    value = models.SlugField(unique=True)
    label = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label


class Booking(models.Model):
    PROPERTY_TYPES = [
        ("residential", "Residential"),
        ("small-business", "Small Business"),
        ("commercial", "Commercial"),
        ("industrial", "Industrial"),
    ]
    TIME_SLOTS = [
        ("morning", "Morning (8 AM – 12 PM)"),
        ("afternoon", "Afternoon (12 PM – 4 PM)"),
        ("evening", "Evening (4 PM – 6 PM)"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    services = models.JSONField(default=list)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=20, choices=TIME_SLOTS)
    address = models.TextField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} — {self.full_name}"


class Project(models.Model):
    PROPERTY_TYPES = [
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("industrial", "Industrial"),
    ]

    title = models.CharField(max_length=160)
    location = models.CharField(max_length=120, default="Freeport, Grand Bahama")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default="commercial")
    summary = models.CharField(max_length=240)
    challenge = models.TextField()
    solution = models.TextField()
    result = models.TextField()
    services = models.JSONField(
        default=list,
        help_text='Tags shown on card, e.g. ["CCTV", "Access Control"]',
    )
    image = models.CharField(
        max_length=200,
        blank=True,
        help_text='Static asset path, e.g. "assets/projects/site-1.jpg" — leave blank for icon placeholder',
    )
    icon = models.CharField(max_length=10, default="📹")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    client_role = models.CharField(
        max_length=160,
        help_text='e.g. "Commercial client, Freeport" or "Homeowner, Lucaya"',
    )
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.client_name} — {self.client_role}"


class FAQ(models.Model):
    question = models.CharField(max_length=240)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
