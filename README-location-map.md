# Coastal Cabana EC - Interactive Location Map

An interactive Google Maps-based location explorer showing nearby amenities, routes, and travel times from Coastal Cabana EC.

## Features

✅ **Category-Based Filtering**: Switch between Shopping & Dining, Parks & Recreation, Schools & Childcare, Healthcare, and Transport  
✅ **Interactive Markers**: Click markers to see routes and travel times  
✅ **Pre-Cached Routes**: Instant route display without API calls using pre-fetched data  
✅ **Hover Information**: Hover over markers to see quick details  
✅ **Route Visualization**: Visual route display with distance and travel times  
✅ **Travel Time Display**: Shows drive time, walk time, and transit time for all locations  
✅ **Responsive Design**: Works on desktop, tablet, and mobile devices

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes:

- Django
- googlemaps (for route pre-fetching)

### 2. Get a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API** (for displaying the map)
   - **Directions API** (for pre-fetching routes)
   - **Geometry API** (for encoding/decoding polylines)
4. Go to **Credentials** and create an API key
5. (Recommended) Restrict your API key:
   - For frontend: Restrict to your domain
   - For backend: Restrict to your server IP

### 3. Configure the API Key

Add your API key to Django settings or environment variables:

```python
# In settings.py or .env
GOOGLE_MAPS_API_KEY = 'your_api_key_here'
```

### 4. Pre-Fetch All Routes (Recommended)

Run the management command to fetch and cache all routes upfront:

```bash
python manage.py fetch_routes
```

This will:

- Fetch routes for all travel modes (driving, walking, transit)
- Store encoded polylines in `coordinates_results.json`
- Save travel times and distances
- Enable instant route display without API calls

Options:

```bash
# Use a specific API key
python manage.py fetch_routes --api-key YOUR_API_KEY

# Adjust delay between requests (default: 0.2 seconds)
python manage.py fetch_routes --delay 0.5
```

### 5. Run the Django Development Server

```bash
python manage.py runserver
```

Navigate to: `http://localhost:8000/location-map/`

## Management Commands

### `fetch_coordinates`

Fetch coordinates for new locations and add them to the JSON file:

```bash
# Add locations to a category
python manage.py fetch_coordinates "Location 1" "Location 2" --category "Shopping & Dining"

# Add MRT stations
python manage.py fetch_coordinates "Tampines MRT" --category "Connectivity - MRT Stations"
```

### `fetch_routes` (New!)

Pre-fetch all routes and cache them in the JSON file:

```bash
# Fetch all routes
python manage.py fetch_routes

# With custom API key
python manage.py fetch_routes --api-key YOUR_KEY

# With slower rate limiting
python manage.py fetch_routes --delay 0.5
```

**Benefits:**

- ✅ Routes load instantly (no API calls needed)
- ✅ Dramatically reduced API costs (one-time fetch vs. every user click)
- ✅ Better user experience (instant vs. 1-2 second wait)
- ✅ Works offline after initial page load

## File Structure

```
Cabana/
├── location_map/
│   ├── management/commands/
│   │   ├── fetch_coordinates.py   # Fetch location coordinates
│   │   └── fetch_routes.py        # Pre-fetch and cache routes
│   ├── static/location_map/
│   │   ├── coordinates_results.json  # Location data + cached routes
│   │   ├── location-map.js          # Frontend JavaScript
│   │   └── location-map.css         # Styling
│   ├── templates/location_map/
│   │   └── index.html               # Main template
│   └── views.py
└── README-location-map.md           # This file
```

## How Routes Are Cached

### JSON Structure

Each location in `coordinates_results.json` now includes `cached_routes`:

```json
{
  "name": "White Sands Mall",
  "lat": 1.3732,
  "lng": 103.9493,
  "cached_routes": {
    "Drive": {
      "encoded_polyline": "encoded_string_here",
      "duration": "5 mins",
      "distance": "1.7 km",
      "duration_value": 300,
      "distance_value": 1700
    },
    "Walk": { ... },
    "Transit": { ... }
  }
}
```

### How It Works

1. **Pre-fetch**: Run `fetch_routes` command once to fetch all routes
2. **Storage**: Routes stored as encoded polylines (space-efficient)
3. **Frontend**: JavaScript decodes polylines and displays instantly
4. **Fallback**: If no cached route, falls back to Directions API

## API Usage & Costs

### With Route Caching (Recommended)

**One-time costs:**

- Run `fetch_routes`: ~$0.50-$2.00 (for 50-200 locations × 3 routes each)

**Ongoing costs:**

- Map loads: Free (within generous free tier)
- Route displays: **$0** (uses cached data)

**Estimated savings:** 99% reduction in API costs

### Without Route Caching

**Per-user costs:**

- Each route click: ~$0.005
- 100 users × 10 clicks = $5.00/day = $150/month

**Verdict:** Route caching pays for itself after ~1 day of traffic!

## How to Use

1. **Select a Category**: Click on any category tab (Shopping & Dining, Parks & Recreation, etc.)
2. **View Locations**: Markers will appear on the map for locations in that category
3. **Hover for Info**: Move your mouse over a marker to see quick information
4. **Click for Route**: Click a marker to see the driving route from Coastal Cabana EC
5. **View Travel Times**: Check the travel info panel below the map for detailed travel information

## Location Data

The map includes data for:

### Shopping & Dining

- Downtown East (0.2km)
- White Sands Mall (1.7km)
- Pasir Ris Mall (1.7km)
- Loyang Point
- Elias Mall

### Parks & Recreation

- Pasir Ris Park (1.5km)
- Pasir Ris Beach
- Pasir Ris Sports Centre

### Schools & Childcare

- Multiple Primary Schools within 1km
- Secondary Schools nearby
- Preschools and Kindergartens

### Healthcare

- Pasir Ris Polyclinic (newly redeveloped)
- 24-hour Clinics
- Supermarkets and Pharmacies

### Transport

- Pasir Ris MRT Station (EW1) - 1.7km
- Future Cross Island Line (CRL) by 2030
- Major Bus Routes

## Customization

### Adding New Locations

Edit `location-map.js` and add locations to the `LOCATIONS` object:

```javascript
"Your Category": [
  {
    name: "Location Name",
    address: "Full Address",
    lat: 1.3724,
    lng: 103.9494,
    description: "Description of the location",
    distance: "1.5km",
    walkTime: "15 min" // optional
  }
]
```

### Changing the Condo Location

Update the `CONDO_LOCATION` constant in `location-map.js`:

```javascript
const CONDO_LOCATION = {
  lat: 1.3851, // Your latitude
  lng: 103.9654, // Your longitude
  name: "Your Location Name",
};
```

### Styling

Modify `location-map.css` to change:

- Colors (search for `#667eea` and `#764ba2` to change the theme)
- Font sizes
- Layout and spacing
- Map height (currently 600px desktop, 400px mobile)

## API Usage & Costs

### Free Tier

Google Maps provides a generous free tier:

- Maps JavaScript API: Free for most use cases
- Directions API: First $200/month free (approximately 40,000 requests)

### Best Practices

- Restrict your API key to your domain
- Enable only the APIs you need
- Monitor usage in Google Cloud Console

## Browser Support

Works in all modern browsers:

- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Map Not Showing

- Check that you've replaced `YOUR_API_KEY` with your actual key
- Verify the Maps JavaScript API is enabled in Google Cloud Console
- Check browser console for error messages

### Routes Not Displaying

- Ensure the Directions API is enabled
- Check that you haven't exceeded API quotas
- Verify coordinates are correct (latitude, longitude format)

### Markers Not Appearing

- Check browser console for JavaScript errors
- Verify location data has valid lat/lng coordinates
- Make sure the `marker` library is loaded in the API script tag

## Credits

- Built with Google Maps JavaScript API
- Location data sourced from official Singapore government sources and verified online sources
- Coordinates obtained using Google Maps and geocoding services

## License

This project is part of the Coastal Cabana EC website.

## Support

For issues or questions about this map implementation, check:

- [Google Maps JavaScript API Documentation](https://developers.google.com/maps/documentation/javascript)
- [Stack Overflow - Google Maps](https://stackoverflow.com/questions/tagged/google-maps)

---

**Note**: Remember to replace `YOUR_API_KEY` with your actual Google Maps API key before deploying to production!
