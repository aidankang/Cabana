# Coastal Cabana EC - Django Project

A Django-based web application for exploring the Coastal Cabana EC location with an interactive Google Maps interface showing nearby amenities, routes, and travel times.

## Features

✅ **Django Web Framework**: Built with Django 5.2 for robust backend functionality  
✅ **Category-Based Filtering**: Switch between Shopping & Dining, Parks & Recreation, Schools & Childcare, Healthcare, and Transport  
✅ **Interactive Google Maps**: Click markers to see routes and travel times  
✅ **Hover Information**: Hover over markers to see quick details  
✅ **Route Visualization**: Visual route display with distance and drive time  
✅ **Travel Time Display**: Shows drive time, walk time, and bus time where available  
✅ **Responsive Design**: Works on desktop, tablet, and mobile devices

## Project Structure

```
Cabana/
├── cabana_project/          # Django project settings
│   ├── settings.py          # Main settings file
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI application
├── location_map/            # Django app for location map
│   ├── static/              # Static files (CSS, JS)
│   ├── templates/           # HTML templates
│   ├── views.py             # View functions
│   └── urls.py              # App URL configuration
├── .venv/                   # Python virtual environment
├── manage.py                # Django management script
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment file
└── README.md                # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Cabana
```

### 2. Set Up Python Virtual Environment

The project uses a Python virtual environment (`.venv`). If it's already created, activate it:

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

If you need to create a new virtual environment:

```bash
python -m venv .venv
```

### 3. Install Dependencies

With the virtual environment activated:

```bash
pip install django python-dotenv
```

Or if there's a requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here
   ```

### 5. Get a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Directions API**
4. Go to **Credentials** and create an API key
5. Add the API key to your `.env` file
6. (Optional) Restrict your API key to your domain for security

### 6. Run Database Migrations

```bash
python manage.py migrate
```

### 7. Create a Superuser (Optional)

To access the Django admin interface:

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

The admin interface will be available at: `http://127.0.0.1:8000/admin/`

## Development

### Project Components

- **Django Project**: `cabana_project/` - Contains project-wide settings and configuration
- **Location Map App**: `location_map/` - Handles the interactive map functionality
- **Static Files**: CSS and JavaScript files are in `location_map/static/location_map/`
- **Templates**: HTML templates are in `location_map/templates/location_map/`

### Adding New Features

1. Create new views in `location_map/views.py`
2. Add URL patterns in `location_map/urls.py`
3. Create templates in `location_map/templates/location_map/`
4. Add static files in `location_map/static/location_map/`

### Running Tests

```bash
python manage.py test
```

## Deployment

Before deploying to production:

1. Set `DEBUG=False` in your environment variables
2. Generate a new `SECRET_KEY` for production
3. Set appropriate `ALLOWED_HOSTS`
4. Configure a production database (PostgreSQL recommended)
5. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
6. Use a production WSGI server like Gunicorn or uWSGI
7. Set up a reverse proxy (Nginx or Apache)

## Additional Documentation

- [Original Location Map Documentation](README-location-map.md)
- [Coastal Cabana EC Sitemap](Coastal_Cabana_EC_Sitemap.md)

## License

[Add your license information here]
