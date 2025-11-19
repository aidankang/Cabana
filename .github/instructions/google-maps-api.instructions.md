# Google Maps JavaScript API - Copilot Instructions

## Overview
This instruction file provides comprehensive guidance for working with the Google Maps JavaScript API. Use this when developing features that integrate Google Maps functionality.

## Official Documentation Reference
- **Main Examples Page**: https://developers.google.com/maps/documentation/javascript/examples
- **Full Documentation**: https://developers.google.com/maps/documentation/javascript
- **API Reference**: https://developers.google.com/maps/documentation/javascript/reference
- **Tutorials**: https://developers.google.com/maps/documentation/javascript/tutorials

## API Categories and Common Use Cases

### 1. Basics
- **[Simple Map](https://developers.google.com/maps/documentation/javascript/examples/map-simple)**: Initialize a basic map
- **[Showing Pixel and Tile Coordinates](https://developers.google.com/maps/documentation/javascript/examples/map-coordinates)**: Display coordinate information
- **[Geolocation](https://developers.google.com/maps/documentation/javascript/examples/map-geolocation)**: Access user's current location
- **[Localizing the Map](https://developers.google.com/maps/documentation/javascript/examples/map-language)**: Support multiple languages
- **[Right-to-Left Languages](https://developers.google.com/maps/documentation/javascript/examples/map-rtl)**: RTL language support
- **[Custom Map Projections](https://developers.google.com/maps/documentation/javascript/examples/map-projection-simple)**: Custom coordinate systems
- **[Lat/Lng Object Literal](https://developers.google.com/maps/documentation/javascript/examples/map-latlng-literal)**: Work with latitude/longitude coordinates

### 2. Events
- **[Simple Click Events](https://developers.google.com/maps/documentation/javascript/examples/event-simple)**: Handle user clicks on the map
- **[Using Closures in Event Listeners](https://developers.google.com/maps/documentation/javascript/examples/event-closure)**: Use closures in event handlers
- **[Accessing Arguments in UI Events](https://developers.google.com/maps/documentation/javascript/examples/event-arguments)**: Access event arguments
- **[Getting Properties With Event Handlers](https://developers.google.com/maps/documentation/javascript/examples/event-properties)**: Retrieve properties from events
- **[Getting Lat/Lng from a Click Event](https://developers.google.com/maps/documentation/javascript/examples/event-click-latlng)**: Extract coordinates from click events
- **[Listening to DOM Events](https://developers.google.com/maps/documentation/javascript/examples/event-domListener)**: Handle DOM events
- **[POI Click Events](https://developers.google.com/maps/documentation/javascript/examples/event-poi)**: Interact with Points of Interest

### 3. Controls and Interaction
- **[Default Controls](https://developers.google.com/maps/documentation/javascript/examples/control-default)**: Zoom, pan, street view controls
- **[Disabling the Default UI](https://developers.google.com/maps/documentation/javascript/examples/control-disableUI)**: Remove default controls
- **[Adding Controls to the Map](https://developers.google.com/maps/documentation/javascript/examples/control-simple)**: Add standard controls
- **[Control Options](https://developers.google.com/maps/documentation/javascript/examples/control-options)**: Configure control behavior
- **[Control Positioning](https://developers.google.com/maps/documentation/javascript/examples/control-positioning)**: Place controls in custom positions
- **[Custom Controls](https://developers.google.com/maps/documentation/javascript/examples/control-custom)**: Build your own UI controls
- **[Adding State to Controls](https://developers.google.com/maps/documentation/javascript/examples/control-custom-state)**: Stateful custom controls
- **[Cooperative Gesture Handling](https://developers.google.com/maps/documentation/javascript/examples/interaction-cooperative)**: Better mobile scrolling and zooming

### 4. Styling and Customization
- **[Styled Map - map ID](https://developers.google.com/maps/documentation/javascript/examples/map-id-style)**: Use map IDs and custom styles
- **[Marker Collision Management](https://developers.google.com/maps/documentation/javascript/examples/marker-collision-management)**: Control marker overlap behavior
- **[Styled Maps - Night Mode](https://developers.google.com/maps/documentation/javascript/examples/style-array)**: Dark theme styling
- **[Styled Map Types](https://developers.google.com/maps/documentation/javascript/examples/maptype-styled-simple)**: Create custom map types
- **[Hiding Map Features With Styling](https://developers.google.com/maps/documentation/javascript/examples/hiding-features)**: Remove unwanted map elements
- **[Styled Map Selection](https://developers.google.com/maps/documentation/javascript/examples/style-selector)**: Switch between style presets

### 5. Markers

#### Advanced Markers (Recommended)
- **[Simple Advanced Markers](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-simple)**: Basic markers with default styling
- **[Basic Marker Customization](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-basic-style)**: Customize marker appearance
- **[Create Markers with Graphics](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-graphics)**: Custom SVG and image markers
- **[Create Markers using HTML and CSS](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-html-simple)**: Simple HTML markers
- **[Create Interactive Markers using HTML and CSS](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-html)**: Rich interactive HTML markers
- **[Animate Markers using CSS](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-animation)**: Animate markers with CSS
- **[Control Marker Collision Behavior](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-collision)**: Control how markers overlap
- **[Set Marker Altitude](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-altitude)**: 3D marker positioning
- **[Control Marker Visibility by Zoom Level](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-zoom)**: Show/hide markers at specific zoom levels
- **[Make Markers Clickable and Accessible](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-accessibility)**: Make markers screen-reader friendly
- **[Make Markers Draggable](https://developers.google.com/maps/documentation/javascript/examples/advanced-markers-draggable)**: Enable marker dragging

#### Legacy Markers
- **[Simple Markers](https://developers.google.com/maps/documentation/javascript/examples/marker-simple)**: Basic legacy markers
- **[Marker Labels](https://developers.google.com/maps/documentation/javascript/examples/marker-labels)**: Add text labels to markers
- **[Removing Markers](https://developers.google.com/maps/documentation/javascript/examples/marker-remove)**: Remove markers from map
- **[Simple Marker Icons](https://developers.google.com/maps/documentation/javascript/examples/icon-simple)**: Basic custom icons
- **[Complex Marker Icons](https://developers.google.com/maps/documentation/javascript/examples/icon-complex)**: Advanced icon customization
- **[Markers with SVG and Font](https://developers.google.com/maps/documentation/javascript/examples/marker-modern)**: SVG and font-based markers
- **[Marker Accessibility](https://developers.google.com/maps/documentation/javascript/examples/marker-accessibility)**: Accessible legacy markers
- **[Marker Animations](https://developers.google.com/maps/documentation/javascript/examples/marker-animations)**: Animate legacy markers
- **[Marker Animations With setTimeout()](https://developers.google.com/maps/documentation/javascript/examples/marker-animations-iteration)**: Delayed animations

*Note: Advanced Markers are preferred for new projects*

### 6. Drawing on the Map
- **[Info Windows](https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple)**: Display information popups
- **[Info Windows With maxWidth](https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple-max)**: Constrain info window width
- **[Custom Popups](https://developers.google.com/maps/documentation/javascript/examples/overlay-popup)**: Custom popup overlays
- **[Simple Polylines](https://developers.google.com/maps/documentation/javascript/examples/polyline-simple)**: Draw lines between points
- **[Removing Polylines](https://developers.google.com/maps/documentation/javascript/examples/polyline-remove)**: Remove polylines from map
- **[Deleting a Vertex](https://developers.google.com/maps/documentation/javascript/examples/delete-vertex-menu)**: Edit polyline vertices
- **[Complex Polylines](https://developers.google.com/maps/documentation/javascript/examples/polyline-complex)**: Multi-segment polylines
- **[Simple Polygons](https://developers.google.com/maps/documentation/javascript/examples/polygon-simple)**: Draw filled shapes
- **[Polygon Arrays](https://developers.google.com/maps/documentation/javascript/examples/polygon-arrays)**: Multiple polygons
- **[Polygon Auto-Completion](https://developers.google.com/maps/documentation/javascript/examples/polygon-autoclose)**: Auto-close polygons
- **[Polygon With Hole](https://developers.google.com/maps/documentation/javascript/examples/polygon-hole)**: Polygons with cutouts
- **[Circles](https://developers.google.com/maps/documentation/javascript/examples/circle-simple)**: Draw circles
- **[Rectangles](https://developers.google.com/maps/documentation/javascript/examples/rectangle-simple)**: Draw rectangles
- **[Rectangle Zoom](https://developers.google.com/maps/documentation/javascript/examples/rectangle-zoom)**: Zoom to rectangle bounds
- **[User-Editable Shapes](https://developers.google.com/maps/documentation/javascript/examples/user-editable-shapes)**: Interactive shape editing
- **[Draggable Polygons](https://developers.google.com/maps/documentation/javascript/examples/polygon-draggable)**: Movable polygons
- **[Listening to Events](https://developers.google.com/maps/documentation/javascript/examples/rectangle-event)**: Shape event handlers
- **[Ground Overlays](https://developers.google.com/maps/documentation/javascript/examples/groundoverlay-simple)**: Image overlays on map
- **[Removing Overlays](https://developers.google.com/maps/documentation/javascript/examples/overlay-remove)**: Remove overlays from map
- **[Custom Overlays](https://developers.google.com/maps/documentation/javascript/examples/overlay-simple)**: Build custom map overlays
- **[Predefined Symbols (Marker)](https://developers.google.com/maps/documentation/javascript/examples/marker-symbol-predefined)**: Built-in marker symbols
- **[Custom Symbols (Marker)](https://developers.google.com/maps/documentation/javascript/examples/marker-symbol-custom)**: Custom marker symbols
- **[Animating Symbols](https://developers.google.com/maps/documentation/javascript/examples/overlay-symbol-animate)**: Animated symbols
- **[Arrow Symbols (Polyline)](https://developers.google.com/maps/documentation/javascript/examples/overlay-symbol-arrow)**: Directional arrows
- **[Custom Symbols (Polyline)](https://developers.google.com/maps/documentation/javascript/examples/overlay-symbol-custom)**: Custom polyline symbols
- **[Dashed Line Symbols (Polyline)](https://developers.google.com/maps/documentation/javascript/examples/overlay-symbol-dashed)**: Dashed lines
- **[Draw on a map using Terra Draw](https://developers.google.com/maps/documentation/javascript/examples/map-drawing-terradraw)**: Advanced drawing library integration

### 7. Layers
- **[KML Layers](https://developers.google.com/maps/documentation/javascript/examples/layer-kml)**: Display KML/KMZ files
- **[KML Feature Details](https://developers.google.com/maps/documentation/javascript/examples/layer-kml-features)**: Access KML feature data
- **[Data Layer: Polygon](https://developers.google.com/maps/documentation/javascript/examples/layer-data-polygon)**: GeoJSON polygon layer
- **[Data Layer: Simple](https://developers.google.com/maps/documentation/javascript/examples/layer-data-simple)**: Basic GeoJSON support
- **[Data Layer: Styling](https://developers.google.com/maps/documentation/javascript/examples/layer-data-style)**: Style GeoJSON features
- **[Data Layer: Event Handling](https://developers.google.com/maps/documentation/javascript/examples/layer-data-event)**: GeoJSON event listeners
- **[Data Layer: Dynamic Styling](https://developers.google.com/maps/documentation/javascript/examples/layer-data-dynamic)**: Dynamic feature styling
- **[Data Layer: Drag and Drop GeoJSON](https://developers.google.com/maps/documentation/javascript/examples/layer-data-dragndrop)**: Import GeoJSON files
- **[Data Layer: Earthquakes](https://developers.google.com/maps/documentation/javascript/examples/layer-data-quakes)**: Real-world data visualization
- **[Heatmaps](https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap)**: Visualize density data
- **[GeoRSS Layers](https://developers.google.com/maps/documentation/javascript/examples/layer-georss)**: Display GeoRSS feeds
- **[Traffic Layer](https://developers.google.com/maps/documentation/javascript/examples/layer-traffic)**: Real-time traffic overlay
- **[Transit Layer](https://developers.google.com/maps/documentation/javascript/examples/layer-transit)**: Public transit overlay
- **[Bicycle Layer](https://developers.google.com/maps/documentation/javascript/examples/layer-bicycling)**: Bike routes overlay
- **[deck.gl ArcLayer](https://developers.google.com/maps/documentation/javascript/examples/deckgl-arclayer)**: 3D arc visualizations
- **[deck.gl ScatterPlot GeoJsonLayer](https://developers.google.com/maps/documentation/javascript/examples/deckgl-points)**: Advanced point visualizations

### 8. Services

#### Geocoding
- **[Geocoding Service](https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple)**: Address to coordinates
- **[Reverse Geocoding](https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse)**: Coordinates to address
- **[Reverse Geocoding by Place ID](https://developers.google.com/maps/documentation/javascript/examples/geocoding-place-id)**: Use Place IDs for accuracy
- **[Geocoding Component Restriction](https://developers.google.com/maps/documentation/javascript/examples/geocoding-component-restriction)**: Limit results by component
- **[Region Code Biasing (ES)](https://developers.google.com/maps/documentation/javascript/examples/geocoding-region-es)**: Bias results to Spain
- **[Region Code Biasing (US)](https://developers.google.com/maps/documentation/javascript/examples/geocoding-region-us)**: Bias results to United States

#### Directions
- **[Directions Service](https://developers.google.com/maps/documentation/javascript/examples/directions-simple)**: Get directions between points
- **[Displaying Text Directions With setPanel()](https://developers.google.com/maps/documentation/javascript/examples/directions-panel)**: Display turn-by-turn instructions
- **[Directions Service (Complex)](https://developers.google.com/maps/documentation/javascript/examples/directions-complex)**: Advanced route options
- **[Travel Modes in Directions](https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes)**: Driving, walking, bicycling, transit
- **[Waypoints in Directions](https://developers.google.com/maps/documentation/javascript/examples/directions-waypoints)**: Multi-stop routes
- **[Draggable Directions](https://developers.google.com/maps/documentation/javascript/examples/directions-draggable)**: Interactive route editing

#### Distance Matrix
- **[Distance Matrix Service](https://developers.google.com/maps/documentation/javascript/examples/distance-matrix)**: Calculate travel distance and time between multiple origins and destinations

#### Elevation
- **[Elevation Service](https://developers.google.com/maps/documentation/javascript/examples/elevation-simple)**: Get elevation data for locations
- **[Showing Elevation Along a Path](https://developers.google.com/maps/documentation/javascript/examples/elevation-paths)**: Elevation profiles for routes

#### Street View
- **[Street View Containers](https://developers.google.com/maps/documentation/javascript/examples/streetview-embed)**: Embed Street View
- **[Street View Side-By-Side](https://developers.google.com/maps/documentation/javascript/examples/streetview-simple)**: Map with Street View
- **[Overlays Within Street View](https://developers.google.com/maps/documentation/javascript/examples/streetview-overlays)**: Add markers to Street View
- **[Street View Events](https://developers.google.com/maps/documentation/javascript/examples/streetview-events)**: Handle Street View interactions
- **[Street View Controls](https://developers.google.com/maps/documentation/javascript/examples/streetview-controls)**: Customize Street View UI
- **[Directly Accessing Street View Data](https://developers.google.com/maps/documentation/javascript/examples/streetview-service)**: Street View service API
- **[Custom Street View Panoramas](https://developers.google.com/maps/documentation/javascript/examples/streetview-custom-simple)**: Custom panorama data
- **[Custom Street View Panorama Tiles](https://developers.google.com/maps/documentation/javascript/examples/streetview-custom-tiles)**: Tiled panoramas
- **[Maximum Zoom Imagery Service](https://developers.google.com/maps/documentation/javascript/examples/maxzoom-simple)**: Get max zoom levels

### 9. Places API

#### Places (New) - Recommended
- **[Text Search (New)](https://developers.google.com/maps/documentation/javascript/examples/place-text-search)**: Search for places by query
- **[Nearby Search (New)](https://developers.google.com/maps/documentation/javascript/examples/place-nearby-search)**: Find places near a location
- **[Place Details](https://developers.google.com/maps/documentation/javascript/examples/place-class)**: Get detailed place information
- **[Place Photos](https://developers.google.com/maps/documentation/javascript/examples/place-photos)**: Access place images
- **[Place Autocomplete Widget](https://developers.google.com/maps/documentation/javascript/examples/place-autocomplete-map)**: Search box with suggestions
- **[Place Autocomplete Element](https://developers.google.com/maps/documentation/javascript/examples/place-autocomplete-element)**: Customizable autocomplete component
- **[Place Autocomplete Data API (simple)](https://developers.google.com/maps/documentation/javascript/examples/place-autocomplete-data-simple)**: Basic autocomplete API
- **[Place Autocomplete Data API (session)](https://developers.google.com/maps/documentation/javascript/examples/place-autocomplete-data-session)**: Session-based autocomplete
- **[Place Autocomplete Address Form](https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-addressform)**: Auto-fill address forms

#### Places Service (Legacy)
- **[Place Searches](https://developers.google.com/maps/documentation/javascript/examples/place-search)**: Search for places (legacy)
- **[Place Details](https://developers.google.com/maps/documentation/javascript/examples/place-details)**: Get place details (legacy)
- **[Place Photos](https://developers.google.com/maps/documentation/javascript/examples/place-photos)**: Access photos (legacy)
- **[Place Search Pagination](https://developers.google.com/maps/documentation/javascript/examples/place-search-pagination)**: Paginate search results
- **[Place Autocomplete](https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete)**: Basic autocomplete (legacy)
- **[Place Autocomplete Hotel Search](https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-hotelsearch)**: Hotel-specific search
- **[Restricting Place Autocomplete to Multiple Countries](https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-multiple-countries)**: Multi-country restriction
- **[Places Search Box](https://developers.google.com/maps/documentation/javascript/examples/places-searchbox)**: Search box widget
- **[Retrieving Autocomplete Predictions](https://developers.google.com/maps/documentation/javascript/examples/places-queryprediction)**: Prediction API
- **[Finding a Place ID](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder)**: Get Place IDs
- **[Locating a Place ID With Reverse Geocoding](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-geocoder)**: Place ID from coordinates

*Note: Newer Places API is preferred for new projects*

### 10. Libraries

#### Drawing Library
- **[Drawing Tools](https://developers.google.com/maps/documentation/javascript/examples/drawing-tools)**: Interactive drawing tools for shapes and markers

#### Geometry Library
- **[Navigation Functions (Heading)](https://developers.google.com/maps/documentation/javascript/examples/geometry-headings)**: Calculate bearings between points
- **[Encoding Methods](https://developers.google.com/maps/documentation/javascript/examples/geometry-encodings)**: Encode/decode polylines
- **[Polygon/Point Relationship With containsLocation()](https://developers.google.com/maps/documentation/javascript/examples/poly-containsLocation)**: Check if point is within polygon

### 11. Advanced Features

#### WebGL Overlays
- **[WebGL Overlays (Native API)](https://developers.google.com/maps/documentation/javascript/examples/webgl/webgl-overlay-simple)**: Low-level WebGL control
- **[WebGL Overlays (ThreeJS wrapper)](https://developers.google.com/maps/documentation/javascript/examples/webgl/threejs-overlay-simple)**: 3D graphics with Three.js
- **[Tilt and Rotation](https://developers.google.com/maps/documentation/javascript/examples/webgl/webgl-tilt-rotation)**: 3D perspective views

#### 3D Maps (Experimental)
- **[Simple Map](https://developers.google.com/maps/documentation/javascript/examples/3d/simple-map)**: Photorealistic 3D map tiles
- **[Polygon](https://developers.google.com/maps/documentation/javascript/examples/3d/polygon)**: 3D polygons
- **[Polyline](https://developers.google.com/maps/documentation/javascript/examples/3d/polyline)**: 3D polylines
- **[Camera restrictions](https://developers.google.com/maps/documentation/javascript/examples/3d/camera-restrictions)**: Limit camera movement
- **[Places](https://developers.google.com/maps/documentation/javascript/examples/3d/places)**: Places integration with 3D

#### Web Components
- **[Add a Map Web Component](https://developers.google.com/maps/documentation/javascript/examples/web-components-map)**: `<gmp-map>` component
- **[Add a Map with Markers using Web Components](https://developers.google.com/maps/documentation/javascript/examples/web-components-markers)**: `<gmp-advanced-marker>` component
- **[Add a Map Web Component with Events](https://developers.google.com/maps/documentation/javascript/examples/web-components-events)**: Event handling with web components

#### Boundaries and Choropleth
- **[Style a boundary polygon](https://developers.google.com/maps/documentation/javascript/examples/boundaries-simple)**: Style boundary polygons
- **[Make a choropleth map](https://developers.google.com/maps/documentation/javascript/examples/boundaries-choropleth)**: Create choropleth visualizations
- **[Handle click events](https://developers.google.com/maps/documentation/javascript/examples/boundaries-click)**: Boundary click events

#### React Google Maps Library
- **[Basic Map](https://developers.google.com/maps/documentation/javascript/examples/rgm-basic-map)**: Official React integration
- **[Place Autocomplete](https://developers.google.com/maps/documentation/javascript/examples/rgm-autocomplete)**: React autocomplete component
- **[Extended Component Library](https://developers.google.com/maps/documentation/javascript/examples/rgm-college-picker)**: Advanced React components

#### MapTypes
- **[Basic Map Types](https://developers.google.com/maps/documentation/javascript/examples/maptype-base)**: Roadmap, satellite, hybrid, terrain
- **[Overlay Map Types](https://developers.google.com/maps/documentation/javascript/examples/maptype-overlay)**: Overlay custom map types
- **[Image Map Types](https://developers.google.com/maps/documentation/javascript/examples/maptype-image)**: Custom image tiles
- **[Overlaying Image Map Types](https://developers.google.com/maps/documentation/javascript/examples/maptype-image-overlay)**: Combine image types
- **[45° Imagery](https://developers.google.com/maps/documentation/javascript/examples/aerial-simple)**: Aerial imagery
- **[Rotating 45° Imagery](https://developers.google.com/maps/documentation/javascript/examples/aerial-rotation)**: Rotate aerial views

#### Address Validation
- **[Simple Address Validation](https://developers.google.com/maps/documentation/javascript/examples/address-validation)**: Validate and standardize addresses

#### Fun
- **[Map Puzzle](https://developers.google.com/maps/documentation/javascript/examples/puzzle)**: Interactive map game

## Best Practices

### API Key Management
- Never hardcode API keys in client-side code
- Use environment variables or secure configuration
- Restrict API keys by HTTP referrer, IP address, or application
- Enable only required APIs to minimize costs and security risks

### Performance Optimization
- Use marker clustering for large numbers of markers
- Implement lazy loading for map components
- Use `collision: 'REQUIRED_AND_HIDES_OPTIONAL'` to manage marker density
- Debounce map events (drag, zoom) when making API calls
- Cache geocoding and place details results

### Modern Approaches
- Prefer **Advanced Markers** over legacy markers
- Use **Places (New)** API instead of legacy Places Service
- Consider **Web Components** for simpler integration
- Use **React Google Maps Library** for React projects

### Accessibility
- Provide text alternatives for map content
- Make markers keyboard accessible
- Use ARIA labels for custom controls
- Ensure sufficient color contrast in styled maps

### Mobile Considerations
- Enable `gestureHandling: 'cooperative'` for better mobile UX
- Design controls for touch interfaces
- Test on various screen sizes and devices
- Consider performance on mobile networks

### Error Handling
- Always check for API load errors
- Handle geocoding and service failures gracefully
- Provide fallback UI when maps fail to load
- Monitor quota limits and usage

## Common Code Patterns

### Basic Map Initialization
```javascript
let map;
async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  map = new Map(document.getElementById("map"), {
    center: { lat: 0, lng: 0 },
    zoom: 8,
    mapId: 'YOUR_MAP_ID' // For advanced markers and styling
  });
}
```

### Advanced Marker
```javascript
const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
const marker = new AdvancedMarkerElement({
  map,
  position: { lat: 0, lng: 0 },
  title: "Marker Title"
});
```

### Loading Multiple Libraries
```javascript
const [{ Map }, { AdvancedMarkerElement }, { places }] = await Promise.all([
  google.maps.importLibrary("maps"),
  google.maps.importLibrary("marker"),
  google.maps.importLibrary("places")
]);
```

## Support Resources
- **Stack Overflow**: http://stackoverflow.com/questions/tagged/google-maps (use `google-maps` tag)
- **GitHub**: https://github.com/googlemaps/
- **Discord Community**: https://discord.gg/f4hvx8Rp2q
- **Issue Tracker**: https://issuetracker.google.com/issues/new?component=188853
- **FAQ**: https://developers.google.com/maps/faq

## Pricing Considerations
- Review pricing at: https://mapsplatform.google.com/pricing/
- Map loads, geocoding, directions, and places have different pricing
- Use the Capabilities Explorer to understand costs: https://developers.google.com/maps/documentation/capabilities-explorer
- Monitor usage in Google Cloud Console
- Set up billing alerts and quotas

## When to Use Each Example
- **Building a store locator**: Use Places API + Markers + Info Windows
- **Route planning app**: Use Directions Service + Draggable Directions
- **Data visualization**: Use Data Layer, Heatmaps, or deck.gl
- **Address collection form**: Use Places Autocomplete Address Form
- **Real estate map**: Use Advanced Markers with HTML content + Polygons for boundaries
- **Delivery tracking**: Use Polylines + Animated Markers + Directions
- **Geographic analysis**: Use Geometry Library + Polygons + containsLocation

## License Information
- Code samples are licensed under Apache 2.0 License
- Documentation content under Creative Commons Attribution 4.0 License
- Last updated: 2025-11-14 UTC

---
*This instruction file helps Copilot provide accurate, up-to-date guidance for Google Maps JavaScript API development.*
