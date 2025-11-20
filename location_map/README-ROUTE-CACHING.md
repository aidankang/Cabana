# Route Caching System

## Overview

The location map now uses **pre-cached routes** stored in `coordinates_results.json` to display routes instantly without making Google Directions API calls on every user click.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Pre-fetch Routes (One-time, server-side)          │
│  Command: python manage.py fetch_routes                     │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │ Condo        │─────▶│ Google Maps  │                    │
│  │ Location     │      │ Directions   │                    │
│  └──────────────┘      │ API          │                    │
│         │              └──────────────┘                    │
│         │                     │                             │
│         ▼                     ▼                             │
│  ┌──────────────────────────────┐                          │
│  │  For each location:          │                          │
│  │  - Fetch driving route       │                          │
│  │  - Fetch walking route       │                          │
│  │  - Fetch transit route       │                          │
│  │  - Encode polylines          │                          │
│  │  - Store in JSON             │                          │
│  └──────────────────────────────┘                          │
│                │                                             │
│                ▼                                             │
│  ┌──────────────────────────────┐                          │
│  │ coordinates_results.json     │                          │
│  │ + cached_routes field        │                          │
│  └──────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Step 2: Frontend Loads Data (Every page load)             │
│                                                              │
│  ┌──────────────────────────────┐                          │
│  │ coordinates_results.json     │                          │
│  │ (includes cached routes)     │                          │
│  └──────────────────────────────┘                          │
│                │                                             │
│                ▼                                             │
│  ┌──────────────────────────────┐                          │
│  │ JavaScript loads JSON        │                          │
│  │ Stores routes in memory      │                          │
│  └──────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Step 3: User Clicks Marker (Instant display)              │
│                                                              │
│  ┌──────────────────────────────┐                          │
│  │ User clicks location marker  │                          │
│  └──────────────────────────────┘                          │
│                │                                             │
│                ▼                                             │
│  ┌──────────────────────────────┐                          │
│  │ Check: cached_routes exist?  │                          │
│  └──────────────────────────────┘                          │
│         │              │                                     │
│    YES  │              │ NO                                 │
│         ▼              ▼                                     │
│  ┌──────────┐   ┌──────────────┐                          │
│  │ Decode   │   │ Call Directions│                         │
│  │ Polyline │   │ API (fallback) │                         │
│  │ Display  │   └──────────────┘                          │
│  │ Instantly│                                               │
│  └──────────┘                                               │
│  ⚡ 0ms      ⏱️ 500-2000ms                                  │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### Pre-fetch All Routes

**Basic usage:**

```bash
python manage.py fetch_routes
```

**With custom API key:**

```bash
python manage.py fetch_routes --api-key YOUR_GOOGLE_MAPS_API_KEY
```

**With slower rate limiting (if hitting quota limits):**

```bash
python manage.py fetch_routes --delay 0.5
```

### Add New Locations

When you add new locations, they won't have cached routes initially:

```bash
# 1. Add new locations
python manage.py fetch_coordinates "New Mall" --category "Shopping & Dining"

# 2. Fetch routes for all locations (including new ones)
python manage.py fetch_routes
```

### Verify Cache Status

Open the location map in your browser and check the console:

```
Location Explorer initialized
Routes: 45/50 locations have pre-cached routes
Run "python manage.py fetch_routes" to cache all routes
```

## Data Structure

### Before Route Caching

```json
{
  "name": "White Sands Mall",
  "title": "White Sands",
  "lat": 1.3732,
  "lng": 103.9493,
  "address": "3 Pasir Ris Central St 3",
  "place_id": "ChIJ...",
  "rating": 4.2,
  "thumbnail": "https://..."
}
```

### After Route Caching

```json
{
  "name": "White Sands Mall",
  "title": "White Sands",
  "lat": 1.3732,
  "lng": 103.9493,
  "address": "3 Pasir Ris Central St 3",
  "place_id": "ChIJ...",
  "rating": 4.2,
  "thumbnail": "https://...",
  "cached_routes": {
    "Drive": {
      "encoded_polyline": "u~vFgs~tRnBqC...",
      "duration": "5 mins",
      "distance": "1.7 km",
      "duration_value": 300,
      "distance_value": 1700
    },
    "Walk": {
      "encoded_polyline": "u~vFgs~tRnBqC...",
      "duration": "18 mins",
      "distance": "1.5 km",
      "duration_value": 1080,
      "distance_value": 1500
    },
    "Transit": {
      "encoded_polyline": "u~vFgs~tRnBqC...",
      "duration": "12 mins",
      "distance": "N/A",
      "duration_value": 720,
      "distance_value": 0
    }
  }
}
```

## Technical Details

### Encoded Polylines

Routes are stored using [Google's Encoded Polyline Algorithm Format](https://developers.google.com/maps/documentation/utilities/polylinealgorithm):

- **Space efficient**: `"u~vFgs~tRnBqC..."` instead of 100+ coordinate pairs
- **Precision**: Maintains accuracy within ~1 meter
- **Decoding**: Uses Geometry Library's `encoding.decodePath()` method

**Example:**

```javascript
// Encoded (compact)
const encoded = "u~vFgs~tRnBqCxDyE";

// Decoded (array of LatLng)
const path = google.maps.geometry.encoding.decodePath(encoded);
// [{lat: 1.3732, lng: 103.9493}, {lat: 1.3734, lng: 103.9495}, ...]
```

### Frontend Logic

```javascript
// 1. Check for cached routes
if (location.cached_routes && Object.keys(location.cached_routes).length > 0) {
  // ✓ Use cached data - instant display
  displayCachedRoute(location.cached_routes);
} else {
  // ⚠ No cache - fall back to API
  fetchRouteFromAPI(location);
}

// 2. Decode and display polyline
const decodedPath = google.maps.geometry.encoding.decodePath(
  location.cached_routes.Drive.encoded_polyline
);

const routePolyline = new google.maps.Polyline({
  path: decodedPath,
  strokeColor: "#4285F4",
  strokeWeight: 5,
  map: map,
});
```

## Performance Comparison

### Without Route Caching

- **User clicks marker** → Wait 500-2000ms → Route displays
- **Every click** = 1 API call
- **100 users × 10 clicks** = 1,000 API calls = ~$5.00

### With Route Caching

- **User clicks marker** → Route displays instantly (0ms)
- **Every click** = 0 API calls
- **100 users × 10 clicks** = 0 API calls = $0.00

### One-Time Pre-fetch Cost

- **50 locations × 3 routes** = 150 API calls = ~$0.75
- **Pays for itself** after just 30 user clicks

## Cost Breakdown

### Google Maps Pricing (as of 2025)

| API                 | Cost per Request | Free Tier                     |
| ------------------- | ---------------- | ----------------------------- |
| Directions API      | $0.005           | $200/month (~40,000 requests) |
| Maps JavaScript API | $0.007 per load  | $200/month (~28,000 loads)    |

### Scenario: 1,000 Monthly Users

**Without caching:**

- 1,000 users × 10 route clicks = 10,000 API calls
- 10,000 × $0.005 = **$50/month**

**With caching:**

- One-time: 50 locations × 3 routes = 150 API calls = $0.75
- Ongoing: 0 API calls = **$0/month**
- **Savings: $50/month = $600/year**

## Maintenance

### When to Re-run fetch_routes

Re-run the command when:

1. **New locations added**: After adding locations via `fetch_coordinates`
2. **Route changes**: If roads/transit routes significantly change (rare)
3. **Transit updates**: Every 3-6 months to update transit schedules
4. **Data cleanup**: If you notice stale or incorrect routes

### Monitoring Cache Status

Check browser console when loading the map:

```
Routes: 45/50 locations have pre-cached routes
```

If < 100% cached, run:

```bash
python manage.py fetch_routes
```

## Troubleshooting

### "No module named 'googlemaps'"

```bash
pip install googlemaps==4.10.0
```

### "API key is required"

Add to settings.py:

```python
GOOGLE_MAPS_API_KEY = 'your_api_key_here'
```

Or pass via command line:

```bash
python manage.py fetch_routes --api-key YOUR_KEY
```

### Routes not displaying on frontend

1. **Check JSON file has cached_routes:**

   ```bash
   cat location_map/static/location_map/coordinates_results.json | grep cached_routes
   ```

2. **Check browser console for errors**

3. **Verify Geometry Library is loaded:**
   Make sure `&libraries=geometry` is in the script tag

### "Route quota exceeded"

Increase delay between requests:

```bash
python manage.py fetch_routes --delay 1.0
```

## References

- [Google Maps Directions API](https://developers.google.com/maps/documentation/directions)
- [Encoded Polyline Algorithm](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)
- [Geometry Library - Encoding Methods](https://developers.google.com/maps/documentation/javascript/examples/geometry-encodings)
- [Google Maps Pricing](https://mapsplatform.google.com/pricing/)

## Summary

✅ **Pre-fetch routes once** with `fetch_routes` command  
✅ **Routes load instantly** from cached data  
✅ **99% cost reduction** on API usage  
✅ **Better UX** with no loading delays  
✅ **Fallback to API** if cache missing

**Run this command now to cache all routes:**

```bash
python manage.py fetch_routes
```
