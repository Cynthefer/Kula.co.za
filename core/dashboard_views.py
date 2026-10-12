from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages as flash
from django.core.cache import cache
from django.views.decorators.http import require_POST

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
from .forms import (
    SiteSettingsForm,
    HeroForm,
    AboutSectionForm,
    MissionForm,
    ServiceCategoryForm,
    ServiceForm,
    EquipmentCategoryForm,
    EquipmentBrandForm,
    PageSEOForm,
    SiteStatForm,
    PartnerForm,
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard-index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect(request.GET.get("next") or "dashboard-index")
        flash.error(request, "Invalid credentials.")
    return render(request, "dashboard/login.html")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("dashboard-login")


def _save_singleton(request, form_class, model_class, template, title, redirect_name):
    instance = model_class.load()
    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        cache.delete(f"singleton:{model_class.__name__.lower()}")
        flash.success(request, "Saved.")
        return redirect(redirect_name)
    return render(
        request,
        template,
        {"form": form, "title": title},
    )


@login_required
def index(request):
    context = {
        "services_count": Service.objects.count(),
        "equipment_brands_count": EquipmentBrand.objects.count(),
        "messages_count": ContactMessage.objects.filter(is_read=False).count(),
        "recent_messages": ContactMessage.objects.all()[:5],
    }
    return render(request, "dashboard/index.html", context)


@login_required
def site_settings(request):
    return _save_singleton(
        request,
        SiteSettingsForm,
        SiteSettings,
        "dashboard/singleton_form.html",
        "Site Settings",
        "dashboard-site",
    )


@login_required
def hero(request):
    return _save_singleton(
        request,
        HeroForm,
        Hero,
        "dashboard/singleton_form.html",
        "Hero Section",
        "dashboard-hero",
    )


@login_required
def about(request):
    return _save_singleton(
        request,
        AboutSectionForm,
        AboutSection,
        "dashboard/singleton_form.html",
        "About Section",
        "dashboard-about",
    )


@login_required
def mission(request):
    return _save_singleton(
        request,
        MissionForm,
        Mission,
        "dashboard/singleton_form.html",
        "Mission",
        "dashboard-mission",
    )


@login_required
def services(request):
    context = {
        "categories": ServiceCategory.objects.prefetch_related("services").all(),
    }
    return render(request, "dashboard/services.html", context)


@login_required
def service_create(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Service created.")
        return redirect("dashboard-services")
    return render(request, "dashboard/form.html", {"form": form, "title": "New Service"})


@login_required
def service_edit(request, pk):
    instance = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Service updated.")
        return redirect("dashboard-services")
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Service"})


@login_required
@require_POST
def service_delete(request, pk):
    get_object_or_404(Service, pk=pk).delete()
    flash.success(request, "Service deleted.")
    return redirect("dashboard-services")


@login_required
def service_categories(request):
    context = {"categories": ServiceCategory.objects.all()}
    return render(request, "dashboard/service_categories.html", context)


@login_required
def service_category_create(request):
    form = ServiceCategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Category created.")
        return redirect("dashboard-service-categories")
    return render(request, "dashboard/form.html", {"form": form, "title": "New Service Category"})


@login_required
def service_category_edit(request, pk):
    instance = get_object_or_404(ServiceCategory, pk=pk)
    form = ServiceCategoryForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Category updated.")
        return redirect("dashboard-service-categories")
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Service Category"})


@login_required
@require_POST
def service_category_delete(request, pk):
    get_object_or_404(ServiceCategory, pk=pk).delete()
    flash.success(request, "Category deleted.")
    return redirect("dashboard-service-categories")


@login_required
def equipment(request):
    context = {
        "categories": EquipmentCategory.objects.prefetch_related("brands").all(),
    }
    return render(request, "dashboard/equipment.html", context)


@login_required
def equipment_category_create(request):
    form = EquipmentCategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Equipment category created.")
        return redirect("dashboard-equipment")
    return render(request, "dashboard/form.html", {"form": form, "title": "New Equipment Category"})


@login_required
def equipment_category_edit(request, pk):
    instance = get_object_or_404(EquipmentCategory, pk=pk)
    form = EquipmentCategoryForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Equipment category updated.")
        return redirect("dashboard-equipment")
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Equipment Category"})


@login_required
@require_POST
def equipment_category_delete(request, pk):
    get_object_or_404(EquipmentCategory, pk=pk).delete()
    flash.success(request, "Equipment category deleted.")
    return redirect("dashboard-equipment")


@login_required
def equipment_brand_create(request):
    form = EquipmentBrandForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Equipment brand created.")
        return redirect("dashboard-equipment")
    return render(request, "dashboard/form.html", {"form": form, "title": "New Equipment Brand"})


@login_required
def equipment_brand_edit(request, pk):
    instance = get_object_or_404(EquipmentBrand, pk=pk)
    form = EquipmentBrandForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Equipment brand updated.")
        return redirect("dashboard-equipment")
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Equipment Brand"})


@login_required
@require_POST
def equipment_brand_delete(request, pk):
    get_object_or_404(EquipmentBrand, pk=pk).delete()
    flash.success(request, "Equipment brand deleted.")
    return redirect("dashboard-equipment")


@login_required
def stats(request):
    form = SiteStatForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Stat added.")
        return redirect("dashboard-stats")
    context = {
        "form": form,
        "items": SiteStat.objects.all(),
    }
    return render(request, "dashboard/stats.html", context)


@login_required
def partners(request):
    form = PartnerForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Partner added.")
        return redirect("dashboard-partners")
    context = {
        "form": form,
        "items": Partner.objects.all(),
    }
    return render(request, "dashboard/partners.html", context)


@login_required
def seo(request):
    instance = PageSEO.objects.first()
    form = PageSEOForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "SEO saved.")
        return redirect("dashboard-seo")
    return render(request, "dashboard/form.html", {"form": form, "title": "Page SEO"})


@login_required
def messages_list(request):
    context = {"items": ContactMessage.objects.all()}
    return render(request, "dashboard/messages.html", context)


@login_required
def message_detail(request, pk):
    instance = get_object_or_404(ContactMessage, pk=pk)
    if not instance.is_read:
        instance.is_read = True
        instance.save(update_fields=["is_read"])
    return render(request, "dashboard/message_detail.html", {"item": instance})