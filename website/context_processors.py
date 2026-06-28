from .models import Partner, SiteSettings

NAV_ITEMS = [
    {"url_name": "home", "label": "Home"},
    {"url_name": "about", "label": "About"},
    {"url_name": "services", "label": "Services"},
    {"url_name": "projects", "label": "Projects"},
    {"url_name": "pricing", "label": "Pricing"},
    {"url_name": "reviews", "label": "Reviews"},
    {"url_name": "faq", "label": "FAQ"},
    {"url_name": "book", "label": "Book Visit"},
    {"url_name": "contact", "label": "Contact"},
]


def site_context(request):
    url_name = ""
    if request.resolver_match:
        url_name = request.resolver_match.url_name or ""
    return {
        "site": SiteSettings.load(),
        "partners": Partner.objects.filter(is_active=True),
        "nav_items": NAV_ITEMS,
        "current_page": url_name,
    }
