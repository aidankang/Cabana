import requests
import json
import time

# SerpAPI Key
API_KEY = "c655abc550a6a266a5dfd5f56bcca097aca2bec8349b2775333952516fecfe69"

def search_location(query):
    """Search for a location using SerpAPI Google Maps"""
    url = "https://serpapi.com/search.json"
    
    params = {
        "engine": "google_maps",
        "q": f"{query}",
        "ll": "@1.3521,103.8198,14z",
        "type": "search",
        "hl":"en",
        "google_domain": "google.com",
        "api_key": API_KEY
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
        
        print(f"No results found for: {query}")
        return None
        
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return None

def main():
    # Condo location
    print("Fetching condo location...")
    condo = search_location("Coastal Cabana EC Pasir Ris")
    
    # All locations to search - simplified names for better matching
    locations = {
        "Shopping & Dining": [
            "Downtown East Pasir Ris",
            "White Sands Shopping Centre Pasir Ris",
            "Pasir Ris Mall",
            "Loyang Point Singapore",
            "Elias Mall Singapore"
        ],
        "Parks & Recreation": [
            "Pasir Ris Park",
            "Pasir Ris Beach",
            "Pasir Ris Sports Centre"
        ],
        "Schools & Childcare": [
            "Casuarina Primary School Singapore",
            "Pasir Ris Primary School",
            "White Sands Primary School Singapore",
            "Hai Sing Catholic School Singapore",
            "Pasir Ris Crest Secondary School",
            "MindChamps PreSchool Pasir Ris Mall",
            "Odyssey The Global Preschool Loyang"
        ],
        "Healthcare": [
            "Pasir Ris Polyclinic",
            "Central 24-HR Clinic Pasir Ris",
            "Cold Storage Pasir Ris Mall",
            "NTUC FairPrice Downtown East"
        ],
        "Transport": [
            "Pasir Ris MRT Station",
            "Pasir Ris Bus Interchange"
        ]
    }
    
    results = {
        "condo": condo,
        "locations": {}
    }
    
    # Fetch coordinates for each category
    for category, places in locations.items():
        print(f"\n--- {category} ---")
        results["locations"][category] = []
        
        for place in places:
            print(f"Fetching: {place}")
            coords = search_location(place)
            if coords:
                results["locations"][category].append(coords)
                print(f"  ✓ Found: {coords['lat']}, {coords['lng']}")
            else:
                print(f"  ✗ Not found")
            
            # Rate limiting - wait 1 second between requests
            time.sleep(1)
    
    # Save results to JSON file
    with open("coordinates_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print("Results saved to coordinates_results.json")
    print("="*60)
    
    # Print summary
    print("\nCONDO LOCATION:")
    if condo:
        print(f"  {condo['title']}")
        print(f"  Coordinates: {condo['lat']}, {condo['lng']}")
    
    print("\nLOCATIONS BY CATEGORY:")
    for category, places in results["locations"].items():
        print(f"\n{category}: {len(places)} locations")
        for place in places:
            print(f"  - {place['title']}: {place['lat']}, {place['lng']}")

if __name__ == "__main__":
    main()
