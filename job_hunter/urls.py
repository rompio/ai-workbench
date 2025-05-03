from django.urls import path
from django.shortcuts import redirect
from .views import (
    dashboard_view,
    personal_data_view,
    ai_assistant_view,
    search_view,
    OfferDeleteView
)
from . import views

app_name = "job_hunter"

urlpatterns = [
    path("", lambda request: redirect("job_hunter:dashboard")),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("personal-data/", personal_data_view, name="personal_data"),
    path("ai-assistant/", ai_assistant_view, name="ai_assistant"),
    path("search/", search_view, name="search"),
    path('offer_list/', views.OfferListView.as_view(), name='offer_list'),
    path(
        "offer/<int:pk>/", views.OfferDetailView.as_view(), name="offer_detail"
    ),
    path(
        "offer/create/", views.OfferCreateView.as_view(), name="offer_create"
    ),
    path(
        "offer/<int:pk>/edit/",
        views.OfferUpdateView.as_view(),
        name="offer_edit",
    ),
    path('offer/<int:pk>/delete/', OfferDeleteView.as_view(), name='offer_delete'),
    path('offer/<int:offer_id>/create-letter/', views.create_letter, name='create_letter'),
    path('offer/<int:offer_id>/view-letter/', views.view_letter, name='view_letter'),
    path('offer/<int:offer_id>/edit-letter/', views.edit_letter, name='edit_letter'),  # Neue URL für Editieren

]
