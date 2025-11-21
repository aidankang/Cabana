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
      mapId: "3efffa2eaac033454501a8ce", // Required for Advanced Markers (styles configured in Cloud Console)
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      zoomControl: false,
    });

    this.map.addListener("click", () => {
      if (window.closeDrawer) window.closeDrawer();
    });
  }

  createCondoMarker() {
    // Create custom HTML for condo marker
    const condoElement = document.createElement("div");
    condoElement.className = "condo-marker";
    condoElement.innerHTML = `
      <div class="pulse-ring"></div>
      <div class="condo-pin">
        <div class="pin-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20">
            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
          </svg>
        </div>
      </div>
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

    // Close drawer if open
    if (window.closeDrawer) window.closeDrawer();

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

    // Store location data with marker for easy access
    marker.locationData = location;

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
      const travelTimes = this.displayCachedRouteOnMap(location.cached_routes);
      this.displayTravelInfo(travelTimes, location);
      this.displayInfoWindow(marker, location, travelTimes, true);
    } else {
      // No cached routes available
      console.log(`No cached routes found for ${location.name}`);
      this.displayInfoWindow(marker, location, null, false);
    }
  }

  displayCachedRouteOnMap(cachedRoutes) {
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
        strokeColor: "#1a1a1a",
        strokeOpacity: 0.8,
        strokeWeight: 4,
        map: this.map,
      });

      // Clear previous route and set new one
      this.directionsRenderer.setDirections({ routes: [] });

      // Store the polyline so we can clear it later
      if (this.currentRoutePolyline) {
        this.currentRoutePolyline.setMap(null);
      }
      this.currentRoutePolyline = routePolyline;

      // Fit map bounds to show the entire route
      const bounds = new google.maps.LatLngBounds();
      decodedPath.forEach((point) => bounds.extend(point));
      // Add some padding so markers aren't on the edge
      this.map.fitBounds(bounds, {
        top: 100,
        bottom: 100,
        left: 50,
        right: 50,
      });
    }

    return travelTimes;
  }

  displayInfoWindow(marker, location, travelTimes, fromCache) {
    let content;

    if (travelTimes) {
      // Build info window content with travel times - mobile-first design
      content = `
        <div class="info-detailed">
          ${
            location.thumbnail
              ? `<img src="${location.thumbnail}" alt="${location.name}" class="info-thumbnail">`
              : ""
          }
          <div class="info-content">
            <h3 class="info-title">${location.name}</h3>
            <p class="info-meta">
              ${
                location.rating
                  ? `<span>${location.rating} <span class="rating-star">★</span></span>`
                  : ""
              }
              ${
                location.description
                  ? `<span>• ${location.description}</span>`
                  : ""
              }
            </p>
            <div class="info-times">
              ${
                travelTimes.Drive
                  ? `<div class="info-time-item">
                      Drive: ${travelTimes.Drive.duration}
                     </div>`
                  : ""
              }
              ${
                travelTimes.Walk
                  ? `<div class="info-time-item">
                      Walk: ${travelTimes.Walk.duration}
                     </div>`
                  : ""
              }
              ${
                travelTimes.Transit
                  ? `<div class="info-time-item">
                      Bus: ${travelTimes.Transit.duration}
                     </div>`
                  : ""
              }
            </div>
          </div>
        </div>
      `;
    } else {
      // No route data available
      content = `
        <div class="info-error">
          ${
            location.thumbnail
              ? `<img src="${location.thumbnail}" alt="${location.name}" class="info-thumbnail">`
              : ""
          }
          <div class="info-content">
            <h3 class="info-title">${location.name}</h3>
            <p class="info-meta">${location.description || ""}${
        location.rating
          ? ` • ${location.rating} <span class="rating-star">★</span>`
          : ""
      }</p>
            <p class="info-hint">Click to see commute times</p>
          </div>
        </div>
      `;
    }

    this.infoWindow.setContent(content);

    // Check if mobile view
    if (window.innerWidth < 768) {
      const drawer = document.getElementById("location-drawer");
      const drawerContent = document.getElementById("drawer-content");

      if (drawer && drawerContent) {
        drawerContent.innerHTML = content;
        drawer.classList.add("visible");
        this.infoWindow.close(); // Ensure popup is closed
      }
    } else {
      this.infoWindow.open(this.map, marker);
      // Ensure drawer is closed on desktop
      const drawer = document.getElementById("location-drawer");
      if (drawer) drawer.classList.remove("visible");
    }
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
      thumbnail: loc.thumbnail || null,
      rating: loc.rating || null,
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

// Global function to close drawer
window.closeDrawer = function () {
  const drawer = document.getElementById("location-drawer");
  if (drawer) {
    drawer.classList.remove("visible");
  }
};
