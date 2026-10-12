from django.core.management.base import BaseCommand
from core.models import (
    SiteSettings,
    Hero,
    AboutSection,
    Mission,
    ServiceCategory,
    Service,
    EquipmentCategory,
    EquipmentBrand,
    PageSEO,
    SiteStat,
    Partner,
)


class Command(BaseCommand):
    help = "Seed initial Kula content"

    def handle(self, *args, **options):
        self.seed_site_settings()
        self.seed_hero()
        self.seed_about()
        self.seed_mission()
        self.seed_service_categories()
        self.seed_services()
        self.seed_equipment()
        self.seed_stats()
        self.seed_seo()
        self.stdout.write(self.style.SUCCESS("Seed complete."))

    def seed_site_settings(self):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "company_name": "KULA AUTO ELECTRICAL ENGINEERING",
                "tagline": "Heavy Duty Auto Electrical Specialists",
                "registration_number": "2025/816562/07",
                "phone_primary": "+27 78 311 8510",
                "phone_secondary": "+27 65 073 2743",
                "email": "admin@kula.co.za",
                "address": "7 Mangoose Street, Esther Park, Johannesburg, 1619",
            },
        )
        self.stdout.write("Site settings seeded.")

    def seed_hero(self):
        Hero.objects.update_or_create(
            pk=1,
            defaults={
                "heading": "Heavy Duty Auto Electrical Engineering",
                "subheading": "Specialised service and repair of heavy-duty auto electrical equipment for earth-moving and mining operations.",
                "cta_text": "Get a Quote",
                "cta_link": "/contact/",
                "secondary_cta_text": "Our Services",
                "secondary_cta_link": "/services/",
            },
        )
        self.stdout.write("Hero seeded.")

    def seed_about(self):
        AboutSection.objects.update_or_create(
            pk=1,
            defaults={
                "title": "About Kula",
                "body": (
                    "<p>KULA AUTO ELECTRICAL ENGINEERING is an auto electrical company "
                    "founded in 2025 by qualified and experienced auto electrical enthusiasts "
                    "who are driven by passion and current automobile technology.</p>"
                    "<p>KULA specialises in service and repair of heavy-duty auto electrical "
                    "equipment, bringing precision and innovation to the earth-moving industry.</p>"
                ),
            },
        )
        self.stdout.write("About seeded.")

    def seed_mission(self):
        Mission.objects.update_or_create(
            pk=1,
            defaults={
                "title": "Our Mission",
                "body": (
                    "<p>Our mission is to serve and provide our customers with quality and "
                    "efficient service while bringing innovation to the automobile industry, "
                    "heavy and earth-moving equipment in particular.</p>"
                ),
            },
        )
        self.stdout.write("Mission seeded.")

    def seed_service_categories(self):
        installation, _ = ServiceCategory.objects.update_or_create(
            slug="installation",
            defaults={
                "name": "Installation",
                "description": "Custom electrical installations built to mining and operational specifications.",
                "order": 1,
            },
        )
        maintenance, _ = ServiceCategory.objects.update_or_create(
            slug="maintenance",
            defaults={
                "name": "Maintenance",
                "description": "Service, repair, and preventative maintenance for heavy-duty auto electrical equipment.",
                "order": 2,
            },
        )
        self.installation_category = installation
        self.maintenance_category = maintenance
        self.stdout.write("Service categories seeded.")

    def seed_services(self):
        installation_services = [
            ("Custom Electrical Components", "Customise electrical components to adhere to mining specification, including seat belt alarms, lighting, and anti-collision systems.", "settings"),
            ("Wiring Harness Fitment", "Fitment of new wiring harnesses.", "cable"),
            ("Smart Camera Systems", "Installation of smart camera systems for equipment monitoring.", "camera"),
            ("Vehicle Monitoring Systems", "Advanced vehicle monitoring systems installation.", "activity"),
            ("After-Market Display Units", "Installation and customisation of after-market display units.", "monitor"),
            ("Auto Braking Systems", "Installation of auto braking systems to suit specific requirements.", "shield"),
        ]
        maintenance_services = [
            ("Heavy Duty Repairs", "Service and repair of heavy-duty auto electrical equipment.", "wrench"),
            ("Preventative Maintenance", "Scheduled preventative maintenance to keep your fleet running.", "calendar-check"),
            ("On-Site Auto Electrical", "Man-on-site duties for auto electrical work.", "user-check"),
            ("Injector Coding & Trims", "Injector coding and trim settings.", "gauge"),
            ("Control Unit Flash Programming", "Control unit flash programming.", "cpu"),
            ("Actuator & Sensor Calibration", "Calibration for actuators and sensors.", "sliders"),
            ("Control Unit Parameter Setting", "Control unit parameter configuration.", "settings-2"),
            ("Component Rebuilds", "Rebuild and repair of electrical components including starter motors, alternators, and repairable electrical valves and control units.", "refresh-cw"),
        ]

        for index, (title, description, icon) in enumerate(installation_services, start=1):
            Service.objects.update_or_create(
                category=self.installation_category,
                title=title,
                defaults={
                    "description": description,
                    "icon": icon,
                    "order": index,
                    "is_active": True,
                },
            )

        for index, (title, description, icon) in enumerate(maintenance_services, start=1):
            Service.objects.update_or_create(
                category=self.maintenance_category,
                title=title,
                defaults={
                    "description": description,
                    "icon": icon,
                    "order": index,
                    "is_active": True,
                },
            )

        self.stdout.write("Services seeded.")

    def seed_equipment(self):
        equipment = [
            ("Excavators", "excavator", [
                "CAT", "Komatsu", "Hyundai", "Hitachi", "Volvo",
                "Kobelco", "Sany", "Doosan", "New Holland", "JCB",
            ]),
            ("Haul Trucks", "truck", [
                "CAT", "Bell", "Komatsu", "Belaz", "Volvo",
            ]),
            ("TLB", "tractor", [
                "CAT", "Bell", "Bobcat", "JCB",
            ]),
            ("Graders", "route", [
                "CAT", "Bell", "Komatsu", "Kobelco", "Volvo",
            ]),
            ("Loaders", "tractor", [
                "CAT", "Bell", "Komatsu", "Hyundai", "Volvo",
                "Hitachi", "Sem", "Lovol", "Leugoug",
            ]),
            ("Telehandlers", "forklift", [
                "JCB", "Kemach", "Bobcat", "Manitou",
            ]),
        ]

        for cat_index, (cat_name, cat_icon, brands) in enumerate(equipment, start=1):
            slug = cat_name.lower().replace(" ", "-")
            category, _ = EquipmentCategory.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": cat_name,
                    "icon": cat_icon,
                    "order": cat_index,
                },
            )
            for brand_index, brand_name in enumerate(brands, start=1):
                EquipmentBrand.objects.update_or_create(
                    category=category,
                    name=brand_name,
                    defaults={
                        "order": brand_index,
                        "is_active": True,
                    },
                )

        self.stdout.write("Equipment seeded.")

    def seed_stats(self):
        stats = [
            ("Heavy Duty Equipment", "100+", "truck"),
            ("Major Brands Serviced", "25+", "award"),
            ("Years Combined Experience", "10+", "clock"),
            ("Customer Satisfaction", "100%", "thumbs-up"),
        ]
        for index, (label, value, icon) in enumerate(stats, start=1):
            SiteStat.objects.update_or_create(
                label=label,
                defaults={
                    "value": value,
                    "icon": icon,
                    "order": index,
                    "is_active": True,
                },
            )
        self.stdout.write("Stats seeded.")

    def seed_seo(self):
        PageSEO.objects.update_or_create(
            page_key="home",
            defaults={
                "page_name": "Home",
                "meta_title": "KULA AUTO ELECTRICAL ENGINEERING | Heavy Duty Auto Electrical Specialists",
                "meta_description": "Specialised service and repair of heavy-duty auto electrical equipment for earth-moving and mining operations in Johannesburg.",
                "keywords": "auto electrical, heavy duty, earth moving, mining equipment, Johannesburg, Kula",
            },
        )
        self.stdout.write("SEO seeded.")