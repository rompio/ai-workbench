from django.shortcuts import render

def dashboard(request):
    return render(request, 'movie_rater/dashboard.html')
