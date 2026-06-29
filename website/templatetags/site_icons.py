from django import template

register = template.Library()

LEGACY_ICON_MAP = {
    "🛡️": "shield",
    "🏢": "building",
    "🎓": "training",
    "📡": "network",
    "📹": "cctv",
    "🔐": "access",
    "🧠": "facial",
    "🔥": "fire",
    "📻": "radio",
    "🖥️": "server",
    "💻": "code",
    "👁️": "monitor",
    "🏗️": "building",
    "💰": "pricing",
    "⭐": "star",
    "❓": "help",
    "📅": "calendar",
    "📍": "map",
    "🕐": "clock",
    "📧": "mail",
    "📞": "phone",
    "💬": "message",
}


@register.filter
def icon_slug(value):
    if not value:
        return "grid"
    key = str(value).strip()
    if key in LEGACY_ICON_MAP:
        return LEGACY_ICON_MAP[key]
    return key


@register.inclusion_tag("website/includes/site_icon.html")
def site_icon(name, size="md"):
    return {"name": icon_slug(name), "size": size}
