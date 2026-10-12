from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from ordered_model.models import OrderedModel

from ..models import (
    SiteSettings,
    Hero,
    AboutSection,
    Mission,
    ServiceCategory,
    Service,
    EquipmentCategory,
    EquipmentBrand,
    PageSEO,
    ContactMessage,
    SiteStat,
    Partner,
)
from .serializers import (
    SiteSettingsSerializer,
    HeroSerializer,
    AboutSectionSerializer,
    MissionSerializer,
    ServiceCategorySerializer,
    ServiceSerializer,
    EquipmentCategorySerializer,
    EquipmentBrandSerializer,
    PageSEOSerializer,
    ContactMessageSerializer,
    SiteStatSerializer,
    PartnerSerializer,
    InlineEditSerializer,
)


class SingletonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return self.model_class.load()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f"singleton:{obj.__class__.__name__.lower()}")
        return Response(serializer.data)


class SiteSettingsViewSet(SingletonViewSet):
    model_class = SiteSettings
    serializer_class = SiteSettingsSerializer
    queryset = SiteSettings.objects.all()


class HeroViewSet(SingletonViewSet):
    model_class = Hero
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()


class AboutViewSet(SingletonViewSet):
    model_class = AboutSection
    serializer_class = AboutSectionSerializer
    queryset = AboutSection.objects.all()


class MissionViewSet(SingletonViewSet):
    model_class = Mission
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related("category").all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__slug=category)
        return qs


class EquipmentCategoryViewSet(viewsets.ModelViewSet):
    queryset = EquipmentCategory.objects.all()
    serializer_class = EquipmentCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EquipmentBrandViewSet(viewsets.ModelViewSet):
    queryset = EquipmentBrand.objects.select_related("category").all()
    serializer_class = EquipmentBrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__slug=category)
        return qs


class PageSEOViewSet(viewsets.ModelViewSet):
    queryset = PageSEO.objects.all()
    serializer_class = PageSEOSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == "create":
            return []
        return [IsAuthenticated()]


class SiteStatViewSet(viewsets.ModelViewSet):
    queryset = SiteStat.objects.all()
    serializer_class = SiteStatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


MODEL_MAP = {
    "site_settings": SiteSettings,
    "hero": Hero,
    "about": AboutSection,
    "mission": Mission,
    "service": Service,
    "service_category": ServiceCategory,
    "equipment_category": EquipmentCategory,
    "equipment_brand": EquipmentBrand,
    "page_seo": PageSEO,
    "site_stat": SiteStat,
    "partner": Partner,
}

SINGLETON_KEYS = {"site_settings", "hero", "about", "mission"}

EDITABLE_FIELDS = {
    "site_settings": {
        "company_name", "tagline", "registration_number", "phone_primary",
        "phone_secondary", "email", "address", "facebook_url", "linkedin_url",
        "instagram_url", "whatsapp_number", "google_maps_embed",
    },
    "hero": {
        "heading", "subheading", "cta_text", "cta_link",
        "secondary_cta_text", "secondary_cta_link",
    },
    "about": {"title", "body"},
    "mission": {"title", "body"},
    "service": {"title", "description", "icon"},
    "service_category": {"name", "description"},
    "equipment_category": {"name", "description", "icon"},
    "equipment_brand": {"name", "website_url"},
    "page_seo": {"meta_title", "meta_description", "keywords"},
    "site_stat": {"label", "value", "icon"},
    "partner": {"name", "website_url"},
}


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def inline_edit(request):
    serializer = InlineEditSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    key = data["model"]
    field = data["field"]
    value = data["value"]

    if field not in EDITABLE_FIELDS.get(key, set()):
        return Response(
            {"detail": "Field not editable."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    model_class = MODEL_MAP.get(key)
    if not model_class:
        return Response(
            {"detail": "Unknown model."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if key in SINGLETON_KEYS:
        obj = model_class.load()
    else:
        object_id = data.get("object_id")
        if not object_id:
            return Response(
                {"detail": "object_id required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = model_class.objects.filter(pk=object_id).first()
        if not obj:
            return Response(
                {"detail": "Object not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    setattr(obj, field, value)
    obj.save()

    if key in SINGLETON_KEYS:
        cache.delete(f"singleton:{model_class.__name__.lower()}")

    return Response({"detail": "Saved.", "field": field, "value": value})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reorder(request):
    model_key = request.data.get("model")
    ordered_ids = request.data.get("order", [])

    model_class = MODEL_MAP.get(model_key)
    if not model_class or not issubclass(model_class, OrderedModel):
        return Response(
            {"detail": "Invalid model for reorder."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for index, pk in enumerate(ordered_ids):
        model_class.objects.filter(pk=pk).update(order=index)

    return Response({"detail": "Reordered."})