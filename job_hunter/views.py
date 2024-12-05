from django.shortcuts import render


def index(request):
    return render(request, "job_hunter/index.html")
