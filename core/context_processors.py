from .models import SiteSettings, PageSEO


def site_settings(request):
    settings_obj = SiteSettings.load()
    return {
        "site": settings_obj,
    }


def page_seo(request):
    key = None
    resolver = request.resolver_match
    if resolver and resolver.url_name:
        key = resolver.url_name
    seo = None
    if key:
        seo = PageSEO.objects.filter(page_key=key).first()
    return {
        "seo": seo,
    }