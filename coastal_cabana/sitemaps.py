from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class CoastalCabanaSitemap(Sitemap):
    """Sitemap for Coastal Cabana static pages."""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Return a list of URL names for the static pages
        return [
            'coastal_cabana:homepage',
            'coastal_cabana:project_overview',
            'coastal_cabana:location',
            'coastal_cabana:site_plan_facilities',
            'coastal_cabana:floor_plans',
            'coastal_cabana:unit_mix_pricing',
            'coastal_cabana:eligibility_guide',
            'coastal_cabana:showflat_booking',
            'coastal_cabana:gallery',
            'coastal_cabana:contact',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        # You can customize this to return actual last modification dates
        # For now, we'll return None to use the current date
        return None

    def priority(self, item):
        # Set different priorities for different pages
        if item == 'coastal_cabana:homepage':
            return 1.0
        elif item in ['coastal_cabana:project_overview', 'coastal_cabana:location']:
            return 0.9
        elif item in ['coastal_cabana:floor_plans', 'coastal_cabana:unit_mix_pricing']:
            return 0.8
        else:
            return 0.7


class LocationMapSitemap(Sitemap):
    """Sitemap for Location Map pages."""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return ['location_map:index']

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return None


class StaticViewSitemap(Sitemap):
    """Sitemap for other static pages."""
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        # Add any other static URLs that don't belong to specific apps
        return ['admin:index']  # You can add more static URLs here

    def location(self, item):
        return reverse(item)