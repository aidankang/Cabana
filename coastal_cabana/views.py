from django.shortcuts import render

def homepage(request):
    """Homepage with hero banner and key project highlights"""
    return render(request, 'coastal_cabana/homepage.html')

def project_overview(request):
    """Project overview with developer info and key selling points"""
    return render(request, 'coastal_cabana/project_overview.html')

def location(request):
    """Location page with map, connectivity, and amenities"""
    return render(request, 'coastal_cabana/location.html')

def site_plan_facilities(request):
    """Site plan and facilities page with amenities list"""
    return render(request, 'coastal_cabana/site_plan_facilities.html')

def floor_plans(request):
    """Floor plans page showing all unit types"""
    return render(request, 'coastal_cabana/floor_plans.html')

def unit_mix_pricing(request):
    """Unit mix and pricing information"""
    return render(request, 'coastal_cabana/unit_mix_pricing.html')

def eligibility_guide(request):
    """Eligibility and purchase guide for EC buyers"""
    return render(request, 'coastal_cabana/eligibility_guide.html')

def showflat_booking(request):
    """Showflat and booking information"""
    return render(request, 'coastal_cabana/showflat_booking.html')

def gallery(request):
    """Image and video gallery"""
    return render(request, 'coastal_cabana/gallery.html')

def contact(request):
    """Contact us page with forms and details"""
    return render(request, 'coastal_cabana/contact.html')
