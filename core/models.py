from django.db import models
from django.core.cache import cache
from django_ckeditor_5.fields import CKEditor5Field
from ordered_model.models import OrderedModel
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(self.cache_key())

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def cache_key(cls):
        return f"singleton:{cls.__name__.lower()}"

    @classmethod
    def load(cls):
        obj = cache.get(cls.cache_key())
        if obj is None:
            obj, _ = cls.objects.get_or_create(pk=1)
            cache.set(cls.cache_key(), obj, 60 * 60)
        return obj


class SiteSettings(SingletonModel):
    company_name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    phone_primary = models.CharField(max_length=30)
    phone_secondary = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    address = models.TextField()
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    logo_thumbnail = ImageSpecField(
        source="logo", processors=[ResizeToFill(200, 200)], format="PNG"
    )
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    google_maps_embed = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name


class Hero(SingletonModel):
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=300, blank=True)
    background_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    background_image_wide = ImageSpecField(
        source="background_image",
        processors=[ResizeToFill(1920, 1080)],
        format="JPEG",
        options={"quality": 85},
    )
    cta_text = models.CharField(max_length=50, blank=True)
    cta_link = models.CharField(max_length=200, blank=True)
    secondary_cta_text = models.CharField(max_length=50, blank=True)
    secondary_cta_link = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return self.heading


class AboutSection(SingletonModel):
    title = models.CharField(max_length=200)
    body = CKEditor5Field(config_name="default")
    image = models.ImageField(upload_to="about/", blank=True, null=True)
    image_display = ImageSpecField(
        source="image", processors=[ResizeToFill(800, 600)], format="JPEG"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return self.title


class Mission(SingletonModel):
    title = models.CharField(max_length=200, default="Our Mission")
    body = CKEditor5Field(config_name="default")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mission"
        verbose_name_plural = "Mission"

    def __str__(self):
        return self.title


class ServiceCategory(OrderedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Service(OrderedModel):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name="services"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    image_thumbnail = ImageSpecField(
        source="image", processors=[ResizeToFill(600, 400)], format="JPEG"
    )
    is_active = models.BooleanField(default=True)
    order_with_respect_to = "category"

    class Meta(OrderedModel.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class EquipmentCategory(OrderedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Equipment Category"
        verbose_name_plural = "Equipment Categories"

    def __str__(self):
        return self.name


class EquipmentBrand(OrderedModel):
    category = models.ForeignKey(
        EquipmentCategory, on_delete=models.CASCADE, related_name="brands"
    )
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    logo_thumbnail = ImageSpecField(
        source="logo", processors=[ResizeToFill(200, 100)], format="PNG"
    )
    website_url = models.URLField(blank=True)
    tags = TaggableManager(blank=True)
    is_active = models.BooleanField(default=True)
    order_with_respect_to = "category"

    class Meta(OrderedModel.Meta):
        verbose_name = "Equipment Brand"
        verbose_name_plural = "Equipment Brands"

    def __str__(self):
        return self.name


class PageSEO(models.Model):
    page_key = models.SlugField(unique=True)
    page_name = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    og_image_display = ImageSpecField(
        source="og_image", processors=[ResizeToFill(1200, 630)], format="JPEG"
    )
    keywords = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Page SEO"
        verbose_name_plural = "Page SEO"

    def __str__(self):
        return self.page_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"


class SiteStat(OrderedModel):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Site Stat"
        verbose_name_plural = "Site Stats"

    def __str__(self):
        return f"{self.label}: {self.value}"


class Partner(OrderedModel):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="partners/")
    logo_display = ImageSpecField(
        source="logo", processors=[ResizeToFill(200, 100)], format="PNG"
    )
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name