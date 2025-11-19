# Coastal Cabana EC - Interactive Location Map

An interactive Google Maps-based location explorer showing nearby amenities, routes, and travel times from Coastal Cabana EC.

## Features

✅ **Category-Based Filtering**: Switch between Shopping & Dining, Parks & Recreation, Schools & Childcare, Healthcare, and Transport  
✅ **Interactive Markers**: Click markers to see routes and travel times  
✅ **Hover Information**: Hover over markers to see quick details  
✅ **Route Visualization**: Visual route display with distance and drive time  
✅ **Travel Time Display**: Shows drive time, walk time, and bus time where available  
✅ **Responsive Design**: Works on desktop, tablet, and mobile devices

## Setup Instructions

### 1. Get a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Directions API**
4. Go to **Credentials** and create an API key
5. (Optional) Restrict your API key to your domain for security

### 2. Configure the API Key

Open `location-map.html` and replace `YOUR_API_KEY` with your actual API key:

```html
<script
  async
  src="https://maps.googleapis.com/maps/api/js?key=YOUR_ACTUAL_API_KEY&libraries=marker&callback=initLocationExplorer"
></script>
```

### 3. Run the Application

Simply open `location-map.html` in a web browser. You can:

- **Open directly**: Double-click the HTML file
- **Use a local server** (recommended):

  ```bash
  # Using Python
  python -m http.server 8000

  # Using Node.js
  npx http-server
  ```

  Then navigate to `http://localhost:8000/location-map.html`

## File Structure

```
Cabana/
├── location-map.html       # Main HTML page
├── location-map.js         # JavaScript implementation
├── location-map.css        # Styling
└── README-location-map.md  # This file
```

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
