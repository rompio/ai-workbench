# cam_manager/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Hier könntest du später Kameradaten aus einer DB holen
    return render(request, 'cam_manager/dashboard.html')
