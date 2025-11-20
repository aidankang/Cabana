import requests
import json
import time
import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = '''Fetch coordinates for locations near Coastal Cabana EC using SerpAPI
    
    Examples:
        python manage.py fetch_coordinates "Pasir Ris Park" "Downtown East" "White Sands Mall"
        python manage.py fetch_coordinates "Pasir Ris Park" "Pasir Ris Beach" --category "Parks & Recreation"
        python manage.py fetch_coordinates "NTUC FairPrice" --condo "Coastal Cabana EC"
        python manage.py fetch_coordinates "School A" "School B" --category "Schools" --condo "My Condo"
    '''

    # SerpAPI Key
    API_KEY = "c655abc550a6a266a5dfd5f56bcca097aca2bec8349b2775333952516fecfe69"

    def add_arguments(self, parser):
        parser.add_argument(
            'locations',
            nargs='+',
            type=str,
            help='Location names to search for (e.g., "Pasir Ris Park" "Downtown East")'
        )
        parser.add_argument(
            '--category',
            type=str,
            default='Searched Locations',
            help='Category name for the searched locations (default: "Searched Locations")'
        )
        parser.add_argument(
            '--condo',
            type=str,
            default='Coastal Cabana EC Pasir Ris',
            help='Condo location to fetch (default: "Coastal Cabana EC Pasir Ris")'
        )

    def search_location(self, query):
        """Search for a location using SerpAPI Google Maps"""
        url = "https://serpapi.com/search.json"
        
        params = {
            "engine": "google_maps",
            "q": f"{query}",
            "ll": "@1.3521,103.8198,14z",
            "type": "search",
            "hl": "en",
            "google_domain": "google.com",
            "api_key": self.API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Try to get coordinates from either place_results or local_results
            first_result = None
            
            if "place_results" in data and "gps_coordinates" in data["place_results"]:
                first_result = data["place_results"]
            elif "local_results" in data and len(data["local_results"]) > 0:
                first_result = data["local_results"][0]
            
            if first_result and "gps_coordinates" in first_result:
                return {
                    "name": query,
                    "title": first_result.get("title", query),
                    "lat": first_result["gps_coordinates"]["latitude"],
                    "lng": first_result["gps_coordinates"]["longitude"],
                    "address": first_result.get("address", ""),
                    "place_id": first_result.get("place_id", "")
                }
            
            self.stdout.write(self.style.WARNING(f"No results found for: {query}"))
            return None
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error searching for {query}: {e}"))
            return None

    def handle(self, *args, **options):
        # Get command arguments
        location_queries = options['locations']
        category_name = options['category']
        condo_query = options['condo']
        
        # Determine the output path
        output_path = os.path.join(
            settings.BASE_DIR,
            'location_map',
            'static',
            'location_map',
            'coordinates_results.json'
        )
        
        # Load existing data if file exists
        existing_data = {"condo": None, "locations": {}}
        if os.path.exists(output_path):
            try:
                with open(output_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                self.stdout.write(self.style.SUCCESS(f"✓ Loaded existing data from {output_path}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠ Could not load existing file: {e}"))
        
        # Check if condo already exists
        if existing_data.get("condo") and existing_data["condo"].get("name") == condo_query:
            self.stdout.write(self.style.SUCCESS(f"✓ Condo already exists: {condo_query} (skipping)"))
            condo = existing_data["condo"]
        else:
            # Fetch condo location
            self.stdout.write(f"Fetching condo location: {condo_query}")
            condo = self.search_location(condo_query)
            if condo:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Found: {condo['lat']}, {condo['lng']}"))
        
        # Start with existing data
        results = {
            "condo": condo,
            "locations": existing_data.get("locations", {})
        }
        
        # Ensure category exists in results
        if category_name not in results["locations"]:
            results["locations"][category_name] = []
        
        # Get existing location names in this category
        existing_names = {loc.get("name") for loc in results["locations"][category_name]}
        
        # Fetch coordinates for provided locations
        self.stdout.write(f"\n--- {category_name} ---")
        
        for place in location_queries:
            # Skip if location already exists in this category
            if place in existing_names:
                self.stdout.write(self.style.SUCCESS(f"✓ {place} already exists (skipping)"))
                continue
            
            self.stdout.write(f"Fetching: {place}")
            coords = self.search_location(place)
            if coords:
                results["locations"][category_name].append(coords)
                self.stdout.write(self.style.SUCCESS(f"  ✓ Found: {coords['lat']}, {coords['lng']}"))
            else:
                self.stdout.write(self.style.WARNING(f"  ✗ Not found"))
            
            # Rate limiting - wait 1 second between requests
            time.sleep(1)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save results to JSON file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS(f"Results saved to {output_path}"))
        self.stdout.write("="*60)
        
        # Print summary
        self.stdout.write("\nCONDO LOCATION:")
        if condo:
            self.stdout.write(f"  {condo['title']}")
            self.stdout.write(f"  Coordinates: {condo['lat']}, {condo['lng']}")
        
        self.stdout.write("\nLOCATIONS BY CATEGORY:")
        for category, places in results["locations"].items():
            self.stdout.write(f"\n{category}: {len(places)} locations")
            for place in places:
                self.stdout.write(f"  - {place['title']}: {place['lat']}, {place['lng']}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully fetched {sum(len(places) for places in results['locations'].values())} locations"))
