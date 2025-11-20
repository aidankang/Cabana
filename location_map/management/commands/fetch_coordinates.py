import requests
import json
import time
import os
import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from pydantic import BaseModel, Field
from gpt import gpt_request


class LocationSubcategory(BaseModel):
    """Structured output model for location subcategorization."""
    subcategory: str = Field(description="Specific subcategory for the location (e.g., 'Shopping Mall', 'Primary School', 'Community Park', 'MRT Station', 'Supermarket', etc.)")
    reasoning: str = Field(description="Brief explanation for why this subcategory was chosen")


class Command(BaseCommand):
    help = '''Fetch coordinates for locations near Coastal Cabana EC using SerpAPI
    
    Examples:
        python manage.py fetch_coordinates "Pasir Ris Park" "Downtown East" "White Sands Mall"
        python manage.py fetch_coordinates "Pasir Ris Park" "Pasir Ris Beach" --category "Parks & Recreation"
        python manage.py fetch_coordinates "NTUC FairPrice" --condo "Coastal Cabana EC"
        python manage.py fetch_coordinates "School A" "School B" --category "Schools" --condo "My Condo"
    '''

    # SerpAPI Key
    API_KEY = "21d97bf1d17bccaf9b9b70da56389ce607d60fcb35bc8406b4c1342cde955aa3"
    
    # Singapore coordinates (default search center)
    SINGAPORE_LAT = 1.3521
    SINGAPORE_LNG = 103.8198

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

    def search_location(self, query, lat=None, lng=None):
        """Search for a location using SerpAPI Google Maps"""
        url = "https://serpapi.com/search.json"
        
        # Use provided coordinates or default to Singapore
        if lat is not None and lng is not None:
            ll_param = f"@{lat},{lng},14z"
        else:
            ll_param = f"@{self.SINGAPORE_LAT},{self.SINGAPORE_LNG},14z"
        
        params = {
            "engine": "google_maps",
            "q": f"{query}",
            "ll": ll_param,
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
                    "place_id": first_result.get("place_id", ""),
                    "rating": first_result.get("rating"),
                    "thumbnail": first_result.get("thumbnail")
                }
            
            self.stdout.write(self.style.WARNING(f"No results found for: {query}"))
            return None
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error searching for {query}: {e}"))
            return None

    async def categorize_locations(self, locations_by_category):
        """
        Use OpenAI GPT to assign subcategories to each location.
        
        Args:
            locations_by_category (dict): Dictionary mapping category names to lists of locations
            
        Returns:
            dict: Updated locations with subcategories added
        """
        self.stdout.write(self.style.SUCCESS("\n--- Categorizing Locations with GPT ---"))
        
        # Prepare batch requests for all locations
        params_list = []
        location_refs = []  # Keep track of which location each request corresponds to
        
        for category, locations in locations_by_category.items():
            for location in locations:
                # Skip if subcategory already exists
                if 'subcategory' in location:
                    self.stdout.write(self.style.SUCCESS(f"✓ {location['title']} already has subcategory: {location['subcategory']}"))
                    continue
                
                # Create GPT request for this location
                params = {
                    'model': 'gpt-4o-mini',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a location categorization expert. Given a location name, address, and category, assign a specific subcategory that best describes the type of place it is.'
                        },
                        {
                            'role': 'user',
                            'content': f"Location: {location['title']}\nAddress: {location.get('address', 'N/A')}\nCategory: {category}\n\nWhat specific subcategory best describes this location?"
                        }
                    ],
                    'response_format': LocationSubcategory,
                    'temperature': 0,
                    'max_tokens': 150
                }
                
                params_list.append(params)
                location_refs.append((category, location))
        
        if not params_list:
            self.stdout.write(self.style.SUCCESS("✓ All locations already categorized"))
            return locations_by_category
        
        # Make concurrent GPT requests
        self.stdout.write(f"Making {len(params_list)} GPT requests...")
        outputs, total_cost = await gpt_request(__name__, params_list)
        
        # Update locations with subcategories
        for i, output in enumerate(outputs):
            category, location = location_refs[i]
            if isinstance(output, LocationSubcategory):
                location['subcategory'] = output.subcategory
                location['subcategory_reasoning'] = output.reasoning
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ {location['title']}: {output.subcategory}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠ Failed to categorize {location['title']}"
                    )
                )
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Categorization complete. Total cost: ${total_cost:.4f}"))
        
        return locations_by_category

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
            # Fetch condo location using Singapore coordinates
            self.stdout.write(f"Fetching condo location: {condo_query}")
            condo = self.search_location(condo_query, lat=self.SINGAPORE_LAT, lng=self.SINGAPORE_LNG)
            if condo:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Found: {condo['lat']}, {condo['lng']}"))
        
        # Get condo coordinates for searching nearby locations
        condo_lat = round(condo['lat'], 4) if condo else self.SINGAPORE_LAT
        condo_lng = round(condo['lng'], 4) if condo else self.SINGAPORE_LNG
        
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
            coords = self.search_location(place, lat=condo_lat, lng=condo_lng)
            if coords:
                results["locations"][category_name].append(coords)
                self.stdout.write(self.style.SUCCESS(f"  ✓ Found: {coords['lat']}, {coords['lng']}"))
            else:
                self.stdout.write(self.style.WARNING(f"  ✗ Not found"))
            
            # Rate limiting - wait 1 second between requests
            time.sleep(1)
        
        # Categorize locations using GPT
        results["locations"] = asyncio.run(self.categorize_locations(results["locations"]))
        
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
                subcategory = f" [{place.get('subcategory', 'N/A')}]" if 'subcategory' in place else ""
                self.stdout.write(f"  - {place['title']}{subcategory}: {place['lat']}, {place['lng']}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully fetched {sum(len(places) for places in results['locations'].values())} locations"))
