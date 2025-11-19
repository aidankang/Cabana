// Coastal Cabana EC Location Explorer
// Interactive map showing nearby amenities with routes and travel times

// Condominium location (Accurate coordinates from Google Maps)
const CONDO_LOCATION = {
  lat: 1.3764688,
  lng: 103.9564391,
  name: "Coastal Cabana EC",
};

// Location data organized by category
const LOCATIONS = {
  "Shopping & Dining": [
    {
      name: "Downtown East",
      address: "1 Pasir Ris Close, Singapore 519599",
      lat: 1.3775631,
      lng: 103.954703,
      description:
        "0.2km away (~3 min walk) - eateries, cinema, Wild Wild Wet water park, E!Hub entertainment complex",
      distance: "0.2km",
      walkTime: "3 min",
    },
    {
      name: "White Sands Mall",
      address: "1 Pasir Ris Central St 3, Singapore 518457",
      lat: 1.3724166,
      lng: 103.94965839999999,
      description: "Major shopping center with supermarkets, retail, dining",
      distance: "1.7km",
      driveTime: "9 min",
    },
    {
      name: "Pasir Ris Mall",
      address: "7 Pasir Ris Central, Singapore 519612",
      lat: 1.3727816,
      lng: 103.9482223,
      description:
        "Opened June 2024, 150+ shops across 4 floors. Retail: Uniqlo, Decathlon, Challenger, Cold Storage, Guardian. Dining: McDonald's, Jollibee, Guzman Y Gomez, Genki Sushi",
      distance: "1.7km",
      driveTime: "9 min",
    },
    {
      name: "Loyang Point",
      address: "258 Pasir Ris Street 21, Singapore 510258",
      lat: 1.3669795,
      lng: 103.96455379999999,
      description: "Shopping center along Pasir Ris Drive 3",
      distance: "~1km",
    },
    {
      name: "Elias Mall",
      address: "625 Elias Road, Singapore 510625",
      lat: 1.3600257,
      lng: 103.8339635,
      description:
        "Neighborhood shopping center - One of four neighborhood centers slated for upgrading under URA Master Plan",
      distance: "~2km",
    },
  ],
  "Parks & Recreation": [
    {
      name: "Pasir Ris Park",
      address: "Pasir Ris Park, Singapore",
      lat: 1.3720588,
      lng: 103.95268,
      description:
        "Coastal park with beach access, park connectors, playgrounds, eateries, fishing pond. Revamped recreational facilities and enhanced coastal park experience planned",
      distance: "1.5km",
      walkTime: "15-20 min",
    },
    {
      name: "Pasir Ris Beach",
      address: "Pasir Ris Beach, Singapore",
      lat: 1.3811,
      lng: 103.95,
      description: "Beachside location with easy beach access",
      distance: "~1.5km",
    },
    {
      name: "Pasir Ris Sports Centre",
      address: "120 Pasir Ris Central, Singapore 519640",
      lat: 1.3740237,
      lng: 103.95149459999999,
      description:
        "Swimming pools, sports hall for badminton, street soccer court, gym",
      distance: "~1.7km",
    },
  ],
  "Schools & Childcare": [
    {
      name: "Casuarina Primary School",
      address: "30 Pasir Ris Street 41, Singapore 518983",
      lat: 1.3725006,
      lng: 103.9570205,
      description: "Primary school within 1km",
      distance: "within 1km",
    },
    {
      name: "Pasir Ris Primary School",
      address: "5 Pasir Ris Street 21, Singapore 518979",
      lat: 1.372403,
      lng: 103.9629666,
      description: "Primary school within 1km",
      distance: "within 1km",
    },
    {
      name: "White Sands Primary School",
      address: "2 Pasir Ris Street 11, Singapore 518450",
      lat: 1.3654492999999999,
      lng: 103.9610714,
      description: "Primary school in Pasir Ris",
      distance: "~1.5km",
    },
    {
      name: "Hai Sing Catholic School",
      address: "9 Pasir Ris Drive 6, Singapore 519388",
      lat: 1.3746261,
      lng: 103.9547645,
      description: "Secondary school approximately 0.9km away",
      distance: "0.9km",
    },
    {
      name: "Pasir Ris Crest Secondary School",
      address: "11 Pasir Ris Street 41, Singapore 518980",
      lat: 1.3728817,
      lng: 103.95941599999999,
      description: "Secondary school in Pasir Ris",
      distance: "~1km",
    },
    {
      name: "MindChamps PreSchool @ Pasir Ris Mall",
      address: "7 Pasir Ris Central #01-23, Singapore 519612",
      lat: 1.3731137999999998,
      lng: 103.9486821,
      description: "Preschool at Pasir Ris Mall",
      distance: "~1.7km",
    },
    {
      name: "Odyssey The Global Preschool",
      address: "191 Jln Loyang Besar, Singapore 509326",
      lat: 1.3797783,
      lng: 103.9623099,
      description: "Preschool near Jalan Loyang Besar",
      distance: "~0.5km",
    },
  ],
  Healthcare: [
    {
      name: "Pasir Ris Polyclinic",
      address: "6 Pasir Ris Drive 8 #1M-01, Singapore 519457",
      lat: 1.3735191,
      lng: 103.9480152,
      description:
        "Newly redeveloped facility at Pasir Ris Mall (opened October 2024). 4 times bigger than previous facility. Services: General practice, dental, physiotherapy, chronic disease management",
      distance: "1.7km",
    },
    {
      name: "Central 24-HR Clinic Pasir Ris",
      address: "446 Pasir Ris Drive 6 #01-122, Singapore 510446",
      lat: 1.3703975,
      lng: 103.9578301,
      description: "24-hour medical clinic in Pasir Ris",
      distance: "~1.2km",
    },
    {
      name: "Cold Storage @ Pasir Ris Mall",
      address: "Pasir Ris Mall #B1-11, Singapore 519612",
      lat: 1.3734587,
      lng: 103.9484921,
      description: "Supermarket at Pasir Ris Mall",
      distance: "1.7km",
    },
    {
      name: "NTUC FairPrice @ E-Hub Downtown East",
      address: "1 Pasir Ris Close, E!Hub, Singapore 519599",
      lat: 1.3759318,
      lng: 103.9554591,
      description: "Supermarket at Downtown East",
      distance: "0.2km",
      walkTime: "3 min",
    },
  ],
  Transport: [
    {
      name: "Pasir Ris MRT Station (EW1)",
      address: "1 Pasir Ris Central St 3, Singapore 518457",
      lat: 1.3732126999999998,
      lng: 103.949277,
      description:
        "Approximately 1.7km from site (~20 min walk, ~9 min drive, ~10-15 min by bus). Direct East-West Line access to city. Future CRL interchange by 2030",
      distance: "1.7km",
      busTime: "10-15 min",
      driveTime: "9 min",
    },
    {
      name: "Pasir Ris Bus Interchange",
      address: "Pasir Ris Bus Interchange, Singapore",
      lat: 1.3735167,
      lng: 103.95015079999999,
      description:
        "Major bus interchange with multiple bus services: 3, 5, 6, 12, 15, 17, 21, 39, 46, 53, 58, 68, 81, 88, 89, 109, and more",
      distance: "1.7km",
    },
  ],
};

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

// Initialize when Google Maps is loaded
function initLocationExplorer() {
  const explorer = new LocationExplorer();
  explorer.init();
}

// Expose to global scope for callback
window.initLocationExplorer = initLocationExplorer;
