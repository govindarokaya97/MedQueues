from django.shortcuts import render


# Create your views here.
def doctor_dashboard(request):
    return render(request, 'doctors/doctor_dashboard.html')