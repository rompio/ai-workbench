from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import Camera, CameraForm
from .forms import CameraForm

@login_required
def add_camera(request):
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            camera = form.save(commit=False)
            camera.user = request.user
            camera.save()
            return redirect('cam_manager:dashboard')
    else:
        form = CameraForm()
    return render(request, 'cam_manager/add_camera.html', {'form': form})

@login_required
def dashboard(request):
    cameras = Camera.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            camera = form.save(commit=False)
            camera.user = request.user
            camera.save()
            return redirect('cam_manager:camera_dashboard')
    else:
        form = CameraForm()

    return render(request, 'cam_manager/dashboard.html', {
        'form': form,
        'cameras': cameras,
    })
