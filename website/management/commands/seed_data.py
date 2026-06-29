from decimal import Decimal

from django.core.management.base import BaseCommand

from website.models import (
    AboutCard,
    Certification,
    FAQ,
    Partner,
    PricingExtra,
    PricingPackage,
    Project,
    Service,
    ServiceOption,
    SiteSettings,
    Testimonial,
    Video,
)


class Command(BaseCommand):
    help = "Load and sync site content for Elite Electronics Solutions"

    def handle(self, *args, **options):
        site, _ = SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "company_name": "Elite Electronics Solutions",
                "tagline": "Security & Life Safety · Freeport, Grand Bahama",
                "hero_subtitle": (
                    "CCTV, access control, fire alarms, SAFR facial recognition, and full systems integration — "
                    "designed, installed, and supported by a local Grand Bahama team. Free site assessments."
                ),
                "contact_email": "lashardcarey@gmail.com",
                "contact_phone": "(242) 375-4179",
                "whatsapp_number": "12423754179",
                "trust_items": [
                    "Free site visits & assessments",
                    "Axis & SAFR authorized partner",
                    "BICSI-certified professionals",
                    "Local Grand Bahama team",
                ],
                "stat_projects": "100+",
                "stat_years": "10+",
                "stat_support": "Local support",
                "hero_commercial_url": "https://www.youtube.com/watch?v=jzTGiqlIgbg",
                "hero_commercial_title": "Watch Our Commercial",
            },
        )
        self.stdout.write(f"Site settings: {site.company_name}")

        about_defaults = [
            ("shield", "Full-Scope Integration", "We design, install, configure, and maintain complete security and life safety ecosystems — CCTV, access control, fire alarms, monitoring, and communications."),
            ("building", "Residential to Commercial", "From small home CCTV setups to large-scale commercial installations across Grand Bahama and beyond — every project gets elite attention."),
            ("training", "Training & Support", "We train your staff on system operation, provide ongoing support, and develop custom software solutions tailored to your facility."),
            ("network", "Infrastructure & Servers", "Copper cabling, optical fiber, microwave, point-to-point links, radio communications, and complete server setups for your network backbone."),
        ]
        for i, (icon, title, desc) in enumerate(about_defaults):
            AboutCard.objects.update_or_create(
                title=title,
                defaults={"icon": icon, "description": desc, "order": i},
            )
        self.stdout.write("Synced about cards")

        service_defaults = [
            ("cctv", "CCTV Systems", "IP and analog surveillance for homes, businesses, and industrial sites. Axis-certified installations with remote viewing and recording.", ["Indoor & outdoor cameras", "NVR/DVR setup", "Remote monitoring"], 0),
            ("access", "Access Control", "Card readers, biometric systems, door controllers, and integrated entry management for secure facilities.", ["Card & fob systems", "Biometric readers", "Time & attendance"], 1),
            ("facial", "SAFR Facial Recognition", "Authorized SAFR reseller and installer from RealNetworks. AI-powered facial recognition for secure access, watchlist matching, and intelligent video analytics.", ["Facial recognition access", "Watchlist & threat detection", "Occupancy analytics"], 2),
            ("fire", "Fire Alarm Systems", "Silent Knight and FireLite fire detection, notification, and monitoring systems for code-compliant life safety.", ["Detection & notification", "Panel programming", "24/7 monitoring"], 3),
            ("radio", "Communications", "Two-way radios, intercoms, and transmission infrastructure including copper, fiber, microwave, and point-to-point links.", ["Radio systems", "Fiber & copper cabling", "Microwave links"], 4),
            ("server", "Server & Network Setup", "Server configuration, network architecture, and infrastructure to support your security and business systems.", ["Server deployment", "Network design", "System integration"], 5),
            ("code", "Software Development", "Custom software solutions for monitoring dashboards, access management, and system automation tailored to your needs.", ["Custom dashboards", "API integrations", "Automation tools"], 6),
            ("monitor", "System Monitoring", "Continuous monitoring of fire alarms, CCTV, and access systems with rapid response and alert management.", ["Central station monitoring", "Alert management", "Health checks"], 7),
            ("training", "Staff Training", "Hands-on training for your team on operating, maintaining, and troubleshooting installed systems.", ["On-site training", "Documentation", "Certification prep"], 8),
        ]
        for icon, title, desc, features, order in service_defaults:
            Service.objects.update_or_create(
                title=title,
                defaults={"icon": icon, "description": desc, "features": features, "order": order, "is_active": True},
            )
        self.stdout.write("Synced services")

        if not PricingPackage.objects.exists():
            packages = [
                ("Residential", Decimal("499"), "+", ["2–4 camera CCTV install", "Basic NVR setup", "Mobile app configuration", "1-year warranty on labor", "Basic staff walkthrough"], False),
                ("Small Business", Decimal("2499"), "+", ["8–16 camera system", "Access control (2–4 doors)", "Network & server setup", "Staff training session", "90-day support included"], True),
                ("Commercial", Decimal("9999"), "+", ["Full-scale CCTV deployment", "Fire alarm integration", "Multi-site monitoring", "Fiber/copper infrastructure", "Ongoing maintenance plans"], False),
            ]
            for i, (tier, price, suffix, features, featured) in enumerate(packages):
                PricingPackage.objects.create(tier_name=tier, price=price, price_suffix=suffix, features=features, is_featured=featured, order=i)
            self.stdout.write("Created pricing packages")

        if not PricingExtra.objects.exists():
            extras = [
                ("Site survey & assessment", "From $150"),
                ("Staff training (half-day)", "From $350"),
                ("Fire alarm panel install", "From $1,800"),
                ("Access control per door", "From $650"),
                ("Fiber run (per drop)", "From $200"),
                ("Monthly monitoring", "From $49/mo"),
                ("Software development", "Custom quote"),
                ("Emergency service call", "From $125/hr"),
            ]
            for i, (name, price) in enumerate(extras):
                PricingExtra.objects.create(name=name, price_label=price, order=i)
            self.stdout.write("Created pricing extras")

        partner_defaults = [
            ("AXIS", "Axis Communications", "Industry-leading IP cameras, video encoders, and network audio solutions for professional surveillance.", "authorized", "assets/partners/axis-authorized.png", 0),
            ("ENS", "ENS Security", "Professional security products and solutions for integrators and installers worldwide.", "reseller", "assets/partners/ens.svg", 1),
            ("SK", "Silent Knight", "Trusted fire alarm control panels and detection devices for commercial life safety applications.", "reseller", "assets/partners/silent-knight.svg", 2),
            ("FL", "FireLite", "Fire alarm panels, detectors, and notification appliances for comprehensive fire protection.", "reseller", "assets/partners/firelite.svg", 3),
            ("SAFR", "SAFR by RealNetworks", "AI-powered facial recognition platform for access control, threat detection, and intelligent video analytics. Authorized reseller and installer.", "installer", "assets/partners/safr.svg", 4),
        ]
        for abbr, name, desc, ptype, logo, order in partner_defaults:
            Partner.objects.update_or_create(
                abbreviation=abbr,
                defaults={
                    "name": name,
                    "description": desc,
                    "partner_type": ptype,
                    "logo": logo,
                    "order": order,
                    "is_active": True,
                },
            )
        self.stdout.write("Synced partners")

        cert_defaults = [
            ("Axis Authorized Partner", "Axis Communications", "Official Axis Communications authorized partner for professional IP video and surveillance solutions.", "assets/partners/axis-authorized.png", "", "partner_badge", 0),
            ("SAFR Authorized Installer", "RealNetworks", "Authorized SAFR reseller and installer for AI-powered facial recognition, access control integration, and intelligent video analytics.", "assets/partners/safr.svg", "", "partner_badge", 1),
            ("BICSI Member", "BICSI", "Member of the global ICT association advancing information and communications technology standards and professional excellence.", "assets/certifications/bicsi-affiliation.png", "", "affiliation", 2),
            ("BICSI Installer 1 (INST1)", "BICSI", "Certified installer for ICT infrastructure including structured cabling, pathways, and communications systems.", "assets/certifications/bicsi-inst1.png", "", "certification", 3),
            ("Advanced CPTED", "NICP — National Institute of Crime Prevention", "Advanced Crime Prevention Through Environmental Design certification for designing safer, more secure built environments.", "assets/certifications/advanced-cpted.png", "", "certification", 4),
            ("CPTED Professional Designation (CPD)", "NICP — National Institute of Crime Prevention", "Professional designation in Crime Prevention Through Environmental Design for secure facility planning and threat reduction.", "assets/certifications/cpted-designation.png", "Oct 25, 2025 - Oct 25, 2029", "certification", 5),
        ]
        for name, issuer, desc, image, valid, category, order in cert_defaults:
            Certification.objects.update_or_create(
                name=name,
                defaults={
                    "issuer": issuer,
                    "description": desc,
                    "image": image,
                    "valid_until": valid,
                    "category": category,
                    "order": order,
                    "is_active": True,
                },
            )
        self.stdout.write("Synced certifications")

        option_defaults = [
            ("cctv", "CCTV Systems", 0),
            ("access-control", "Access Control", 1),
            ("safr", "SAFR Facial Recognition", 2),
            ("fire-alarm", "Fire Alarm", 3),
            ("monitoring", "Monitoring", 4),
            ("communications", "Communications", 5),
            ("networking", "Networking / Servers", 6),
            ("training", "Staff Training", 7),
            ("software", "Software Development", 8),
        ]
        for value, label, order in option_defaults:
            ServiceOption.objects.update_or_create(
                value=value,
                defaults={"label": label, "order": order, "is_active": True},
            )
        self.stdout.write("Synced booking options")

        if not Project.objects.exists():
            projects = [
                (
                    "Multi-Camera Commercial Surveillance",
                    "commercial",
                    "Downtown Freeport",
                    "16-camera Axis IP system with remote viewing for a retail plaza.",
                    "Legacy analog cameras with poor coverage and no remote access.",
                    "Designed coverage map, installed Axis cameras, NVR, and mobile app access.",
                    "Full perimeter coverage, 30-day recording, staff trained same day.",
                    ["CCTV", "Axis", "Remote viewing"],
                    "cctv",
                    True,
                ),
                (
                    "Residential SAFR & Access Upgrade",
                    "residential",
                    "Lucaya, Grand Bahama",
                    "Facial recognition entry and CCTV for a private residence.",
                    "Keys and basic intercom only — no audit trail or smart alerts.",
                    "SAFR facial recognition at main entry plus 6-camera CCTV integration.",
                    "Secure family access, visitor logs, and phone notifications.",
                    ["SAFR", "Access Control", "CCTV"],
                    "facial",
                    True,
                ),
                (
                    "Fire Alarm & Life Safety Retrofit",
                    "commercial",
                    "Freeport Industrial Area",
                    "Silent Knight fire detection and notification for a small warehouse.",
                    "Outdated panel not meeting current life safety requirements.",
                    "New Silent Knight panel, detection devices, horn/strobes, and testing.",
                    "Code-compliant system with documented inspection and staff walkthrough.",
                    ["Fire Alarm", "Silent Knight", "Life Safety"],
                    "fire",
                    False,
                ),
            ]
            for i, (title, ptype, loc, summary, challenge, solution, result, tags, icon, featured) in enumerate(projects):
                Project.objects.update_or_create(
                    title=title,
                    defaults={
                        "property_type": ptype,
                        "location": loc,
                        "summary": summary,
                        "challenge": challenge,
                        "solution": solution,
                        "result": result,
                        "services": tags,
                        "icon": icon,
                        "is_featured": featured,
                        "order": i,
                    },
                )
            self.stdout.write("Synced sample projects")
        else:
            project_icons = {
                "Multi-Camera Commercial Surveillance": "cctv",
                "Residential SAFR & Access Upgrade": "facial",
                "Fire Alarm & Life Safety Retrofit": "fire",
            }
            for title, icon in project_icons.items():
                Project.objects.filter(title=title).update(icon=icon)
            self.stdout.write("Synced project icons")

        if not Testimonial.objects.exists():
            testimonials = [
                (
                    "Marcus T.",
                    "Small business owner, Freeport",
                    "Professional from start to finish. They mapped our entire property, installed cameras and access control, and trained my staff the same day.",
                    5,
                ),
                (
                    "Denise H.",
                    "Homeowner, Lucaya",
                    "We wanted better security after moving to Grand Bahama. EES explained every option clearly and the SAFR entry system works flawlessly.",
                    5,
                ),
                (
                    "Operations Manager",
                    "Commercial facility, Grand Bahama",
                    "Reliable local team — fast response, clean installs, and they handle fire alarm and CCTV under one roof. Highly recommend.",
                    5,
                ),
            ]
            for i, (name, role, quote, rating) in enumerate(testimonials):
                Testimonial.objects.create(
                    client_name=name,
                    client_role=role,
                    quote=quote,
                    rating=rating,
                    order=i,
                )
            self.stdout.write("Created testimonials")
        else:
            self.stdout.write("Testimonials already exist — skipping")

        faq_defaults = [
            (
                "Do you serve residential and commercial clients?",
                "Yes. We install everything from home CCTV and access control to full commercial deployments across Freeport, Grand Bahama, and The Bahamas.",
            ),
            (
                "How much does a CCTV system cost?",
                "Residential packages start around $499+ depending on camera count and site layout. Commercial systems are quoted after a free on-site assessment.",
            ),
            (
                "Do you offer free site visits?",
                "Yes. We provide free on-site assessments so we can recommend the right cameras, access points, cabling, and fire safety coverage for your property.",
            ),
            (
                "Which brands do you install?",
                "We are authorized partners for Axis, SAFR by RealNetworks, Silent Knight, FireLite, ENS, and other leading security and life safety platforms.",
            ),
            (
                "How long does installation take?",
                "Small residential jobs may take 1–2 days. Larger commercial projects are scheduled in phases — we give you a clear timeline after the site survey.",
            ),
            (
                "Do you provide training and ongoing support?",
                "Absolutely. We train your staff on day-to-day operation and offer support, maintenance plans, and emergency service calls.",
            ),
            (
                "Are you based locally in Grand Bahama?",
                "Yes. Elite Electronics Solutions is based at Millennium Mall in Freeport with a local team — not outsourced overseas support.",
            ),
            (
                "How do I book a site visit?",
                "Use the booking form on this website, call (242) 375-4179, or message us on WhatsApp. We confirm within 24 hours.",
            ),
        ]
        for i, (question, answer) in enumerate(faq_defaults):
            FAQ.objects.update_or_create(
                question=question,
                defaults={"answer": answer, "order": i, "is_active": True},
            )
        self.stdout.write("Synced FAQs")

        video_defaults = [
            (
                "https://www.youtube.com/watch?v=9GuwGX7fbMo",
                "Elite Electronics Solutions Showcase",
                "See our security and life safety work in Grand Bahama.",
                "projects",
                1,
            ),
            (
                "https://www.youtube.com/watch?v=qd0RZdTPXrU",
                "Installation Highlights",
                "Project footage from the field — cameras, systems, and integrations.",
                "projects",
                0,
            ),
        ]
        for url, title, description, page, order in video_defaults:
            Video.objects.update_or_create(
                youtube_url=url,
                defaults={
                    "title": title,
                    "description": description,
                    "page": page,
                    "order": order,
                    "is_active": True,
                },
            )
        self.stdout.write("Synced videos")
        Video.objects.filter(page="home").update(is_active=False)

        self.stdout.write(self.style.SUCCESS("All content synced successfully."))
