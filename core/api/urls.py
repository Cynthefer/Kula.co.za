from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("site-settings", views.SiteSettingsViewSet, basename="site-settings")
router.register("hero", views.HeroViewSet, basename="hero")
router.register("about", views.AboutViewSet, basename="about")
router.register("mission", views.MissionViewSet, basename="mission")
router.register("service-categories", views.ServiceCategoryViewSet, basename="service-categories")
router.register("services", views.ServiceViewSet, basename="services")
router.register("equipment-categories", views.EquipmentCategoryViewSet, basename="equipment-categories")
router.register("equipment-brands", views.EquipmentBrandViewSet, basename="equipment-brands")
router.register("page-seo", views.PageSEOViewSet, basename="page-seo")
router.register("contact-messages", views.ContactMessageViewSet, basename="contact-messages")
router.register("site-stats", views.SiteStatViewSet, basename="site-stats")
router.register("partners", views.PartnerViewSet, basename="partners")

urlpatterns = [
    path("", include(router.urls)),
    path("inline-edit/", views.inline_edit, name="inline-edit"),
    path("reorder/", views.reorder, name="reorder"),
]