from django.shortcuts import render
from django.conf import settings


def index(request):
    """Render the location map page."""
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'location_map/index.html', context)
