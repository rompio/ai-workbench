from django.shortcuts import render

def dashboard(request):
    return render(request, 'health_tracker/dashboard.html')
