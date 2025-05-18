from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from food.utils import get_raw_foods

def search_food(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        raw_foods = get_raw_foods()
        results = [
            {"id": food[0], "name": food[1]}
            for food in raw_foods
            if query.lower() in food[1].lower()
        ]

    return JsonResponse({"results": results})


@login_required
def overview(request):
    if not request.user.is_pro:
        return render(request, 'users/pro_required.html')
    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    return render(request, 'week_planner/overview.html', {'days': days})


@login_required
def create_plan(request):
    return render(request, "week_planner/create_plan.html")
