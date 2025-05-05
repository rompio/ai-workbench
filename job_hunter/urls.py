from django.urls import path
from django.shortcuts import redirect

from .views import (
    dashboard_view,
    personal_data_view,
    ai_assistant_view,
    search_view,
    create_letter,
    view_letter,
    edit_letter,
    OfferListView,
    OfferDetailView,
    OfferCreateView,
    OfferUpdateView,
    OfferDeleteView,
)


app_name = "job_hunter"

urlpatterns = [
    path("", lambda request: redirect("job_hunter:dashboard")),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("personal-data/", personal_data_view, name="personal_data"),
    path("ai-assistant/", ai_assistant_view, name="ai_assistant"),
    path("search/", search_view, name="search"),
    path("offer_list/", OfferListView.as_view(), name="offer_list"),
    path(
        "offer/<int:pk>/", OfferDetailView.as_view(), name="offer_detail"
    ),
    path(
        "offer/create/", OfferCreateView.as_view(), name="offer_create"
    ),
    path(
        "offer/<int:pk>/edit/",
        OfferUpdateView.as_view(),
        name="offer_edit",
    ),
    path(
        "offer/<int:pk>/delete/",
        OfferDeleteView.as_view(),
        name="offer_delete",
    ),
    path(
        "offer/<int:offer_id>/create-letter/",
        create_letter,
        name="create_letter",
    ),
    path(
        "offer/<int:offer_id>/view-letter/",
        view_letter,
        name="view_letter",
    ),
    path(
        "offer/<int:offer_id>/edit-letter/",
        edit_letter,
        name="edit_letter",
    ),  
]
