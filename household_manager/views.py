from django.shortcuts import render

def dashboard(request):
    return render(request, 'household_manager/dashboard.html')
