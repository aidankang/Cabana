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
  }

  async init() {
    try {
      // Initialize map
      await this.initMap();

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
      mapTypeControl: true,
      streetViewControl: true,
      fullscreenControl: true,
      zoomControl: true,
      gestureHandling: "cooperative",
    });
  }

  createCondoMarker() {
    const marker = new google.maps.Marker({
      position: CONDO_LOCATION,
      map: this.map,
      title: CONDO_LOCATION.name,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 12,
        fillColor: "#FF5722",
        fillOpacity: 1,
        strokeColor: "#FFFFFF",
        strokeWeight: 3,
      },
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
    const marker = new google.maps.Marker({
      position: { lat: location.lat, lng: location.lng },
      map: this.map,
      title: location.name,
      label: {
        text: number.toString(),
        color: "#FFFFFF",
        fontWeight: "bold",
      },
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 16,
        fillColor: "#4285F4",
        fillOpacity: 1,
        strokeColor: "#FFFFFF",
        strokeWeight: 3,
      },
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
        ${
          location.distance
            ? `<p><strong>Distance:</strong> ${location.distance}</p>`
            : ""
        }
        <p class="info-hint">Click to see route</p>
      </div>
    `;

    this.infoWindow.setContent(content);
    this.infoWindow.open(this.map, marker);
  }

  showRoute(marker, location) {
    const request = {
      origin: CONDO_LOCATION,
      destination: { lat: location.lat, lng: location.lng },
      travelMode: google.maps.TravelMode.DRIVING,
    };

    this.directionsService
      .route(request)
      .then((result) => {
        this.directionsRenderer.setDirections(result);
        this.displayTravelInfo(result, location);

        // Show detailed info in info window
        const route = result.routes[0];
        const leg = route.legs[0];

        const content = `
          <div class="info-detailed">
            <h3>${location.name}</h3>
            <p class="address">${location.address || ""}</p>
            <p class="description">${location.description}</p>
            <div class="info-stats">
              <div><strong>Distance:</strong> ${leg.distance.text}</div>
              <div><strong>Drive Time:</strong> ${leg.duration.text}</div>
              ${
                location.walkTime
                  ? `<div><strong>Walk:</strong> ${location.walkTime}</div>`
                  : ""
              }
              ${
                location.busTime
                  ? `<div><strong>Bus:</strong> ${location.busTime}</div>`
                  : ""
              }
            </div>
          </div>
        `;

        this.infoWindow.setContent(content);
        this.infoWindow.open(this.map, marker);
      })
      .catch((e) => {
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
      });
  }

  displayTravelInfo(result, location) {
    const route = result.routes[0];
    const leg = route.legs[0];

    const panel = document.getElementById("travel-details");
    panel.innerHTML = `
      <div class="travel-route">
        <h4>Route to ${location.name}</h4>
        <div class="travel-stats">
          <div class="stat">
            <span class="stat-label">Distance</span>
            <span class="stat-value">${leg.distance.text}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Drive Time</span>
            <span class="stat-value">${leg.duration.text}</span>
          </div>
        </div>
        <p class="route-note">Route displayed on map in blue</p>
        ${
          location.walkTime
            ? `<p class="extra-info"><strong>Walk:</strong> ${location.walkTime}</p>`
            : ""
        }
        ${
          location.busTime
            ? `<p class="extra-info"><strong>Bus:</strong> ${location.busTime}</p>`
            : ""
        }
      </div>
    `;
  }

  clearMarkers() {
    this.markers.forEach((marker) => marker.setMap(null));
    this.markers = [];
  }

  clearRoute() {
    this.directionsRenderer.setDirections({ routes: [] });
    const panel = document.getElementById("travel-details");
    panel.innerHTML =
      '<p class="info-message">Click on a marker to see route and travel time from Coastal Cabana EC</p>';
  }

  fitBounds() {
    const bounds = new google.maps.LatLngBounds();
    bounds.extend(CONDO_LOCATION);
    this.markers.forEach((marker) => {
      bounds.extend(marker.getPosition());
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
  explorer.init();
}

// Expose to global scope for callback
window.initLocationExplorer = initLocationExplorer;
