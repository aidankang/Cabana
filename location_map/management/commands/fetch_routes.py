"""
Django management command to pre-fetch all routes from condo to locations
and update coordinates_results.json with cached route data.
"""
import json
import os
import time
import googlemaps
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = '''Pre-fetch all routes from condo to locations and cache them in coordinates_results.json
    
    This command fetches routes for all travel modes (driving, walking, transit) between
    the condo and all locations in the JSON file, then stores the encoded polylines and
    travel information for instant loading without API calls.
    
    Examples:
        python manage.py fetch_routes
        python manage.py fetch_routes --api-key YOUR_GOOGLE_MAPS_API_KEY
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='Google Maps API key (defaults to GOOGLE_MAPS_API_KEY from settings)'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=0.2,
            help='Delay in seconds between API requests (default: 0.2)'
        )

    def get_api_key(self, options):
        """Get API key from command line or settings"""
        api_key = options.get('api_key')
        if not api_key:
            api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        
        if not api_key:
            raise ValueError(
                "Google Maps API key is required. "
                "Provide via --api-key or set GOOGLE_MAPS_API_KEY in settings"
            )
        
        return api_key

    def fetch_route(self, gmaps_client, origin, destination, mode):
        """
        Fetch a single route using Google Maps Directions API
        
        Args:
            gmaps_client: Google Maps client instance
            origin: Origin coordinates as (lat, lng) tuple
            destination: Destination coordinates as (lat, lng) tuple
            mode: Travel mode ('driving', 'walking', 'transit')
            
        Returns:
            dict: Route data with encoded polyline and travel info, or None if failed
        """
        try:
            result = gmaps_client.directions(
                origin=origin,
                destination=destination,
                mode=mode,
                departure_time='now' if mode == 'transit' else None
            )
            
            if not result or len(result) == 0:
                return None
            
            route = result[0]
            leg = route['legs'][0]
            
            return {
                'encoded_polyline': route['overview_polyline']['points'],
                'duration': leg['duration']['text'],
                'distance': leg.get('distance', {}).get('text', 'N/A'),
                'duration_value': leg['duration']['value'],  # in seconds
                'distance_value': leg.get('distance', {}).get('value', 0)  # in meters
            }
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"  ⚠ Failed to fetch {mode} route: {str(e)}")
            )
            return None

    def fetch_all_routes_for_location(self, gmaps_client, condo_coords, location, delay=0.2):
        """
        Fetch all travel modes (driving, walking, transit) for a single location
        
        Args:
            gmaps_client: Google Maps client instance
            condo_coords: Condo coordinates as (lat, lng) tuple
            location: Location dict with lat/lng
            delay: Delay between API requests in seconds
            
        Returns:
            dict: Route cache data for all travel modes
        """
        routes = {}
        
        destination = (location['lat'], location['lng'])
        
        for mode in ['driving', 'walking', 'transit']:
            route_data = self.fetch_route(gmaps_client, condo_coords, destination, mode)
            
            if route_data:
                # Capitalize first letter for consistency with frontend
                mode_key = mode.capitalize() if mode != 'transit' else 'Transit'
                if mode_key == 'Driving':
                    mode_key = 'Drive'
                elif mode_key == 'Walking':
                    mode_key = 'Walk'
                
                routes[mode_key] = route_data
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    ✓ {mode_key}: {route_data['duration']} ({route_data['distance']})"
                    )
                )
            
            # Rate limiting
            time.sleep(delay)
        
        return routes

    def handle(self, *args, **options):
        # Get API key
        try:
            api_key = self.get_api_key(options)
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return
        
        # Initialize Google Maps client
        gmaps_client = googlemaps.Client(key=api_key)
        
        # Get delay
        delay = options['delay']
        
        # Determine the file path
        json_path = os.path.join(
            settings.BASE_DIR,
            'location_map',
            'static',
            'location_map',
            'coordinates_results.json'
        )
        
        # Load existing data
        if not os.path.exists(json_path):
            self.stdout.write(
                self.style.ERROR(f"File not found: {json_path}")
            )
            return
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error loading JSON file: {e}")
            )
            return
        
        # Get condo coordinates
        if not data.get('condo'):
            self.stdout.write(
                self.style.ERROR("No condo data found in JSON file")
            )
            return
        
        condo = data['condo']
        condo_coords = (condo['lat'], condo['lng'])
        
        self.stdout.write("="*60)
        self.stdout.write(self.style.SUCCESS("PRE-FETCHING ROUTES"))
        self.stdout.write("="*60)
        self.stdout.write(f"Origin: {condo['title']}")
        self.stdout.write(f"Coordinates: {condo_coords}")
        self.stdout.write("")
        
        # Track statistics
        total_locations = 0
        total_routes_fetched = 0
        total_routes_failed = 0
        
        # Iterate through all categories and locations
        for category, locations in data['locations'].items():
            self.stdout.write(f"\n--- {category} ({len(locations)} locations) ---")
            
            for location in locations:
                location_name = location.get('title') or location.get('name')
                self.stdout.write(f"  {location_name}")
                
                # Fetch routes for this location
                routes = self.fetch_all_routes_for_location(
                    gmaps_client,
                    condo_coords,
                    location,
                    delay=delay
                )
                
                # Store routes in location data
                location['cached_routes'] = routes
                
                # Update statistics
                total_locations += 1
                total_routes_fetched += len(routes)
                total_routes_failed += (3 - len(routes))  # 3 modes expected
        
        # Save updated data back to file
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.stdout.write("\n" + "="*60)
            self.stdout.write(self.style.SUCCESS(f"✓ Routes saved to {json_path}"))
            self.stdout.write("="*60)
            
            # Print summary
            self.stdout.write("\nSUMMARY:")
            self.stdout.write(f"  Total locations: {total_locations}")
            self.stdout.write(f"  Routes fetched: {total_routes_fetched}")
            self.stdout.write(f"  Routes failed: {total_routes_failed}")
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Successfully pre-cached routes for {total_locations} locations"
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error saving JSON file: {e}")
            )
