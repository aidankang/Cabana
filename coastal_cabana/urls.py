from django.urls import path
from . import views

app_name = 'coastal_cabana'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('project-overview/', views.project_overview, name='project_overview'),
    path('location/', views.location, name='location'),
    path('site-plan-facilities/', views.site_plan_facilities, name='site_plan_facilities'),
    path('floor-plans/', views.floor_plans, name='floor_plans'),
    path('unit-mix-pricing/', views.unit_mix_pricing, name='unit_mix_pricing'),
    path('eligibility-guide/', views.eligibility_guide, name='eligibility_guide'),
    path('showflat-booking/', views.showflat_booking, name='showflat_booking'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
]