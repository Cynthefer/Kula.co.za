from rest_framework import serializers
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


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"
        read_only_fields = ["updated_at"]


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = "__all__"
        read_only_fields = ["updated_at"]


class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = "__all__"
        read_only_fields = ["updated_at"]


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = "__all__"
        read_only_fields = ["updated_at"]


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ["order"]


class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = "__all__"


class EquipmentBrandSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = EquipmentBrand
        fields = "__all__"
        read_only_fields = ["order"]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class PageSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSEO
        fields = "__all__"
        read_only_fields = ["updated_at"]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["is_read", "created_at"]


class SiteStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStat
        fields = "__all__"
        read_only_fields = ["order"]


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"
        read_only_fields = ["order"]


class InlineEditSerializer(serializers.Serializer):
    model = serializers.ChoiceField(
        choices=[
            "site_settings",
            "hero",
            "about",
            "mission",
            "service",
            "service_category",
            "equipment_category",
            "equipment_brand",
            "page_seo",
            "site_stat",
            "partner",
        ]
    )
    object_id = serializers.IntegerField(required=False, allow_null=True)
    field = serializers.CharField()
    value = serializers.CharField(allow_blank=True)