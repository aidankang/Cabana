// Coastal Cabana EC Location Explorer
// Interactive map showing nearby amenities with routes and travel times

// Global variables to hold location data (will be populated from JSON)
let CONDO_LOCATION = null;
let LOCATIONS = {};

// Main application class
class LocationExplorer {
  constructor() {
    this.map = null;
    this.directionsService = null;
    this.directionsRenderer = null;
    this.markers = [];
    this.condoMarker = null;
    this.infoWindow = null;
    this.currentCategory = "Shopping & Dining";
    this.geometryLibrary = null; // For encoding/decoding polylines
  }

  async init() {
    try {
      // Initialize map
      await this.initMap();

      // Load geometry library for polyline encoding/decoding
      this.geometryLibrary = await google.maps.importLibrary("geometry");

      // Load marker library for AdvancedMarkerElement
      const markerLibrary = await google.maps.importLibrary("marker");
      this.AdvancedMarkerElement = markerLibrary.AdvancedMarkerElement;

      // Initialize services
      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer({
        map: this.map,
        suppressMarkers: true,
        polylineOptions: {
          strokeColor: "#4285F4",
          strokeWeight: 5,
          strokeOpacity: 0.7,
        },
      });

      // Initialize info window
      this.infoWindow = new google.maps.InfoWindow();

      // Create condo marker
      this.createCondoMarker();

      // Setup event listeners
      this.setupCategoryTabs();

      // Show default category
      this.showCategory(this.currentCategory);
    } catch (error) {
      console.error("Error initializing map:", error);
    }
  }

  async initMap() {
    const { Map } = await google.maps.importLibrary("maps");

    this.map = new Map(document.getElementById("map"), {
      center: CONDO_LOCATION,
      zoom: 14,
      mapId: "e57770696a6bd1c9cae8181e", // Required for Advanced Markers (styles configured in Cloud Console)
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      zoomControl: false,
    });
  }

  createCondoMarker() {
    // Create custom HTML for condo marker
    const condoElement = document.createElement("div");
    condoElement.className = "condo-marker";
    condoElement.innerHTML = `
      <div class="marker-pin condo-pin"></div>
    `;

    const marker = new this.AdvancedMarkerElement({
      position: CONDO_LOCATION,
      map: this.map,
      title: CONDO_LOCATION.name,
      content: condoElement,
      zIndex: 1000,
    });

    marker.addListener("click", () => {
      this.infoWindow.setContent(`
        <div class="info-window">
          <h3>${CONDO_LOCATION.name}</h3>
          <p><strong>Your Home</strong></p>
          <p>Click on location markers to see routes and travel times</p>
        </div>
      `);
      this.infoWindow.open(this.map, marker);
    });

    this.condoMarker = marker;
  }

  setupCategoryTabs() {
    const tabs = document.querySelectorAll(".category-tab");

    tabs.forEach((tab) => {
      tab.addEventListener("click", (e) => {
        const category = e.currentTarget.dataset.category;

        // Update active state
        tabs.forEach((t) => t.classList.remove("active"));
        e.currentTarget.classList.add("active");

        // Show category
        this.showCategory(category);
      });
    });
  }

  showCategory(categoryName) {
    this.currentCategory = categoryName;
    const locations = LOCATIONS[categoryName] || [];

    // Clear existing markers and route
    this.clearMarkers();
    this.clearRoute();

    // Create markers for category
    locations.forEach((location, index) => {
      this.createLocationMarker(location, index + 1);
    });

    // Fit map to show all markers
    this.fitBounds();
  }

  createLocationMarker(location, number) {
    // Create custom HTML marker with label
    const markerElement = document.createElement("div");
    markerElement.className = "location-marker";
    markerElement.innerHTML = `
      <div class="marker-label">${location.name}</div>
      <div class="marker-pin"></div>
    `;

    const marker = new this.AdvancedMarkerElement({
      position: { lat: location.lat, lng: location.lng },
      map: this.map,
      title: location.name,
      content: markerElement,
    });

    // Hover interaction
    marker.addListener("mouseover", () => {
      this.showHoverInfo(marker, location);
    });

    marker.addListener("mouseout", () => {
      this.infoWindow.close();
    });

    // Click interaction - show route
    marker.addListener("click", () => {
      this.showRoute(marker, location);
    });

    this.markers.push(marker);
  }

  showHoverInfo(marker, location) {
    const content = `
      <div class="info-hover">
        <h4>${location.name}</h4>
        <p class="info-description">${location.description}</p>
        <p class="info-hint">Click to see commute times (drive, walk, transit)</p>
      </div>
    `;

    this.infoWindow.setContent(content);
    this.infoWindow.open(this.map, marker);
  }

  async showRoute(marker, location) {
    // Check if we have pre-cached route data in the location object
    if (
      location.cached_routes &&
      Object.keys(location.cached_routes).length > 0
    ) {
      console.log(`Using pre-cached route for ${location.name}`);
      this.displayCachedRoute(marker, location, location.cached_routes);
      return;
    }

    // No cache - request from Directions API (fallback)
    console.log(
      `No cached routes found - fetching from API for ${location.name}`
    );

    // Request all three travel modes in parallel
    const travelModes = [
      { mode: google.maps.TravelMode.DRIVING, label: "Drive" },
      { mode: google.maps.TravelMode.WALKING, label: "Walk" },
      { mode: google.maps.TravelMode.TRANSIT, label: "Transit" },
    ];

    const requests = travelModes.map(({ mode }) => ({
      origin: CONDO_LOCATION,
      destination: { lat: location.lat, lng: location.lng },
      travelMode: mode,
    }));

    try {
      // Get all routes simultaneously
      const results = await Promise.allSettled(
        requests.map((request) => this.directionsService.route(request))
      );

      // Extract travel times
      const travelTimes = {};

      results.forEach((result, index) => {
        const modeLabel = travelModes[index].label;
        if (result.status === "fulfilled") {
          const leg = result.value.routes[0].legs[0];
          travelTimes[modeLabel] = {
            duration: leg.duration.text,
            distance: leg.distance.text,
          };
        } else {
          travelTimes[modeLabel] = null;
        }
      });

      // Display the driving route on the map
      if (results[0].status === "fulfilled") {
        this.directionsRenderer.setDirections(results[0].value);
      }

      // Display travel info in panel and info window
      this.displayTravelInfo(travelTimes, location);

      // Build info window content with all travel modes
      const content = `
        <div class="info-detailed">
          <h3>${location.name}</h3>
          <p class="address">${location.address || ""}</p>
          <p class="description">${location.description}</p>
          <div class="info-stats">
            ${
              travelTimes.Drive
                ? `
              <div><strong>🚗 Drive:</strong> ${travelTimes.Drive.duration} (${travelTimes.Drive.distance})</div>
            `
                : "<div><strong>🚗 Drive:</strong> Not available</div>"
            }
            ${
              travelTimes.Walk
                ? `
              <div><strong>🚶 Walk:</strong> ${travelTimes.Walk.duration} (${travelTimes.Walk.distance})</div>
            `
                : "<div><strong>🚶 Walk:</strong> Not available</div>"
            }
            ${
              travelTimes.Transit
                ? `
              <div><strong>🚌 Transit:</strong> ${travelTimes.Transit.duration}</div>
            `
                : "<div><strong>🚌 Transit:</strong> Not available</div>"
            }
          </div>
          <p class="cache-note" style="font-size: 0.8rem; color: #666; margin-top: 8px;">⚠ Loaded from API (consider running fetch_routes command)</p>
        </div>
      `;

      this.infoWindow.setContent(content);
      this.infoWindow.open(this.map, marker);
    } catch (e) {
      console.error("Directions request failed:", e);
      this.infoWindow.setContent(`
        <div class="info-error">
          <h4>${location.name}</h4>
          <p>Route information unavailable</p>
          <p style="font-size: 0.85rem; color: #999;">Error: ${
            e.message || "Unknown error"
          }</p>
        </div>
      `);
      this.infoWindow.open(this.map, marker);
    }
  }

  displayCachedRoute(marker, location, cachedRoutes) {
    // Convert cached route format to travel times format
    const travelTimes = {};
    for (const [mode, routeData] of Object.entries(cachedRoutes)) {
      if (routeData && routeData.duration) {
        travelTimes[mode] = {
          duration: routeData.duration,
          distance: routeData.distance || "N/A",
        };
      }
    }

    // Display the driving route using cached encoded polyline
    if (cachedRoutes.Drive && cachedRoutes.Drive.encoded_polyline) {
      const decodedPath = this.geometryLibrary.encoding.decodePath(
        cachedRoutes.Drive.encoded_polyline
      );

      // Create a polyline from the decoded path
      const routePolyline = new google.maps.Polyline({
        path: decodedPath,
        geodesic: true,
        strokeColor: "#4285F4",
        strokeOpacity: 0.7,
        strokeWeight: 5,
        map: this.map,
      });

      // Clear previous route and set new one
      this.directionsRenderer.setDirections({ routes: [] });

      // Store the polyline so we can clear it later
      if (this.currentRoutePolyline) {
        this.currentRoutePolyline.setMap(null);
      }
      this.currentRoutePolyline = routePolyline;
    }

    // Display travel info in panel and info window
    this.displayTravelInfo(travelTimes, location);

    // Build info window content
    const content = `
      <div class="info-detailed">
        <h3>${location.name}</h3>
        <p class="address">${location.address || ""}</p>
        <p class="description">${location.description}</p>
        <div class="info-stats">
          ${
            travelTimes.Drive
              ? `
            <div><strong>🚗 Drive:</strong> ${travelTimes.Drive.duration} (${travelTimes.Drive.distance})</div>
          `
              : "<div><strong>🚗 Drive:</strong> Not available</div>"
          }
          ${
            travelTimes.Walk
              ? `
            <div><strong>🚶 Walk:</strong> ${travelTimes.Walk.duration} (${travelTimes.Walk.distance})</div>
          `
              : "<div><strong>🚶 Walk:</strong> Not available</div>"
          }
          ${
            travelTimes.Transit
              ? `
            <div><strong>🚌 Transit:</strong> ${travelTimes.Transit.duration}</div>
          `
              : "<div><strong>🚌 Transit:</strong> Not available</div>"
          }
        </div>
        <p class="cache-note" style="font-size: 0.8rem; color: #666; margin-top: 8px;">✓ Loaded from cache</p>
      </div>
    `;

    this.infoWindow.setContent(content);
    this.infoWindow.open(this.map, marker);
  }

  displayTravelInfo(travelTimes, location) {
    const panel = document.getElementById("travel-details");
    panel.innerHTML = `
      <div class="travel-route">
        <h4>Route to ${location.name}</h4>
        <div class="travel-stats">
          ${
            travelTimes.Drive
              ? `
            <div class="stat">
              <span class="stat-label">🚗 Drive</span>
              <span class="stat-value">${travelTimes.Drive.duration}</span>
              <span class="stat-distance">${travelTimes.Drive.distance}</span>
            </div>
          `
              : ""
          }
          ${
            travelTimes.Walk
              ? `
            <div class="stat">
              <span class="stat-label">🚶 Walk</span>
              <span class="stat-value">${travelTimes.Walk.duration}</span>
              <span class="stat-distance">${travelTimes.Walk.distance}</span>
            </div>
          `
              : ""
          }
          ${
            travelTimes.Transit
              ? `
            <div class="stat">
              <span class="stat-label">🚌 Transit</span>
              <span class="stat-value">${travelTimes.Transit.duration}</span>
            </div>
          `
              : ""
          }
        </div>
        <p class="route-note">Driving route displayed on map in blue</p>
      </div>
    `;
  }

  clearMarkers() {
    this.markers.forEach((marker) => {
      marker.map = null; // AdvancedMarkerElement uses .map property instead of .setMap()
    });
    this.markers = [];
  }

  clearRoute() {
    this.directionsRenderer.setDirections({ routes: [] });

    // Clear any cached polyline we created
    if (this.currentRoutePolyline) {
      this.currentRoutePolyline.setMap(null);
      this.currentRoutePolyline = null;
    }

    const panel = document.getElementById("travel-details");
    panel.innerHTML =
      '<p class="info-message">Click on a marker to see route and travel time from Coastal Cabana EC</p>';
  }

  fitBounds() {
    const bounds = new google.maps.LatLngBounds();
    bounds.extend(CONDO_LOCATION);
    this.markers.forEach((marker) => {
      bounds.extend(marker.position);
    });
    this.map.fitBounds(bounds);

    // Prevent excessive zoom for single markers
    const listener = google.maps.event.addListener(this.map, "idle", () => {
      if (this.map.getZoom() > 16) this.map.setZoom(16);
      google.maps.event.removeListener(listener);
    });
  }
}

// Load location data from JSON file
async function loadLocationData() {
  try {
    const response = await fetch(
      "/static/location_map/coordinates_results.json"
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error loading location data:", error);
    return null;
  }
}

// Transform JSON data to match expected format
function transformLocationData(jsonData) {
  // Set condo location
  CONDO_LOCATION = {
    lat: jsonData.condo.lat,
    lng: jsonData.condo.lng,
    name: jsonData.condo.title || jsonData.condo.name,
  };

  // Transform locations by category
  // Use JSON categories directly
  LOCATIONS = {};

  for (const [category, locations] of Object.entries(jsonData.locations)) {
    LOCATIONS[category] = locations.map((loc) => ({
      name: loc.title || loc.name,
      address: loc.address,
      lat: loc.lat,
      lng: loc.lng,
      description: loc.subcategory || "",
      cached_routes: loc.cached_routes || null, // Include cached routes from JSON
    }));
  }

  console.log("Transformed location data:", { CONDO_LOCATION, LOCATIONS });
}

// Initialize when Google Maps is loaded
async function initLocationExplorer() {
  // Load JSON data
  const jsonData = await loadLocationData();

  if (jsonData) {
    console.log("Loaded location data from JSON");
    transformLocationData(jsonData);
  } else {
    console.error(
      "Failed to load location data - map may not function correctly"
    );
    return;
  }

  const explorer = new LocationExplorer();
  await explorer.init();

  // Expose to global scope for debugging
  window.locationExplorer = explorer;
  console.log(
    "Location Explorer initialized. Access via window.locationExplorer"
  );

  // Count cached routes
  let cachedCount = 0;
  let totalCount = 0;
  for (const locations of Object.values(LOCATIONS)) {
    for (const loc of locations) {
      totalCount++;
      if (loc.cached_routes && Object.keys(loc.cached_routes).length > 0) {
        cachedCount++;
      }
    }
  }
  console.log(
    `Routes: ${cachedCount}/${totalCount} locations have pre-cached routes`
  );
  if (cachedCount < totalCount) {
    console.log('Run "python manage.py fetch_routes" to cache all routes');
  }
}

// Expose to global scope for callback
window.initLocationExplorer = initLocationExplorer;
