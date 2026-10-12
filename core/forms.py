from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
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


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault(
                    "class",
                    "w-5 h-5 rounded border-gray-300 text-kula-blue focus:ring-kula-blue",
                )
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault(
                    "class",
                    "w-full rounded-lg border-gray-300 focus:border-kula-blue focus:ring-kula-blue bg-white",
                )
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault(
                    "class",
                    "w-full rounded-lg border-gray-300 focus:border-kula-blue focus:ring-kula-blue",
                )
                widget.attrs.setdefault("rows", 4)
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault(
                    "class",
                    "block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-kula-blue file:text-white hover:file:bg-kula-dark",
                )
            else:
                widget.attrs.setdefault(
                    "class",
                    "w-full rounded-lg border-gray-300 focus:border-kula-blue focus:ring-kula-blue",
                )


class SiteSettingsForm(StyledModelForm):
    class Meta:
        model = SiteSettings
        fields = "__all__"


class HeroForm(StyledModelForm):
    class Meta:
        model = Hero
        fields = "__all__"


class AboutSectionForm(StyledModelForm):
    class Meta:
        model = AboutSection
        fields = "__all__"
        widgets = {"body": CKEditor5Widget(config_name="default")}


class MissionForm(StyledModelForm):
    class Meta:
        model = Mission
        fields = "__all__"
        widgets = {"body": CKEditor5Widget(config_name="default")}


class ServiceCategoryForm(StyledModelForm):
    class Meta:
        model = ServiceCategory
        fields = ["name", "slug", "description"]


class ServiceForm(StyledModelForm):
    class Meta:
        model = Service
        fields = [
            "category",
            "title",
            "description",
            "icon",
            "image",
            "is_active",
        ]


class EquipmentCategoryForm(StyledModelForm):
    class Meta:
        model = EquipmentCategory
        fields = ["name", "slug", "description", "icon"]


class EquipmentBrandForm(StyledModelForm):
    class Meta:
        model = EquipmentBrand
        fields = [
            "category",
            "name",
            "logo",
            "website_url",
            "tags",
            "is_active",
        ]


class PageSEOForm(StyledModelForm):
    class Meta:
        model = PageSEO
        fields = "__all__"


class SiteStatForm(StyledModelForm):
    class Meta:
        model = SiteStat
        fields = ["label", "value", "icon", "is_active"]


class PartnerForm(StyledModelForm):
    class Meta:
        model = Partner
        fields = ["name", "logo", "website_url", "is_active"]


class ContactMessageForm(StyledModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter a valid name.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < 10:
            raise forms.ValidationError("Message is too short.")
        return message