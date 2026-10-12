from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import (
    Hero,
    AboutSection,
    Mission,
    ServiceCategory,
    Service,
    EquipmentCategory,
    EquipmentBrand,
    SiteStat,
    Partner,
    ContactMessage,
)
from .forms import ContactMessageForm


def home(request):
    context = {
        "hero": Hero.load(),
        "about": AboutSection.load(),
        "mission": Mission.load(),
        "service_categories": ServiceCategory.objects.prefetch_related("services").all(),
        "equipment_categories": EquipmentCategory.objects.prefetch_related("brands").all(),
        "stats": SiteStat.objects.filter(is_active=True),
        "partners": Partner.objects.filter(is_active=True),
    }
    return render(request, "home.html", context)


def about(request):
    context = {
        "about": AboutSection.load(),
        "mission": Mission.load(),
        "stats": SiteStat.objects.filter(is_active=True),
    }
    return render(request, "about.html", context)


def services(request):
    context = {
        "service_categories": ServiceCategory.objects.prefetch_related("services").all(),
    }
    return render(request, "services.html", context)


def equipment(request):
    context = {
        "equipment_categories": EquipmentCategory.objects.prefetch_related("brands").all(),
    }
    return render(request, "equipment.html", context)


def contact(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"detail": "Message sent."})
            messages.success(request, "Message sent. We will be in touch shortly.")
            return redirect("contact")
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors}, status=400)
    context = {
        "form": form,
    }
    return render(request, "contact.html", context)


def health(request):
    return JsonResponse({"status": "ok"})