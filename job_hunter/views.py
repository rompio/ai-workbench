from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Offer, PInfo, Application
from .forms import PInfoForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import connection
from django.urls import reverse_lazy
from .forms import OfferForm, ApplicationForm
from django.views.generic import DeleteView
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
import openai
from .utils import generate_application_letter

@login_required
def edit_letter(request, offer_id):
    # Hole das Angebot und stelle sicher, dass der Benutzer zu diesem Angebot gehört
    offer = get_object_or_404(Offer, id=offer_id, user=request.user)

    # Hole die zugehörige Application-Instanz für den Benutzer und das Angebot
    letter = get_object_or_404(Application, offer=offer, user=request.user)

    # Wenn das Formular gesendet wird, speichern wir die Änderungen
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=letter)
        if form.is_valid():
            form.save()
            return redirect('job_hunter:view_letter', offer_id=offer.id)
    else:
        form = ApplicationForm(instance=letter)

    return render(request, 'offers/edit_letter.html', {
        'form': form,
        'offer': offer
    })

@login_required
def create_letter(request, offer_id):
    # Holen der Offer-Daten und Sicherstellen, dass der Benutzer zu diesem Angebot gehört
    offer = get_object_or_404(Offer, id=offer_id, user=request.user)

    # Persönliche Daten abrufen
    pinfo = PInfo.objects.filter(user=request.user).first()
    if not pinfo:
        # Optional: Weiterleitung oder Fehlermeldung, falls keine persönlichen Daten vorhanden sind
        return redirect('job_hunter:personal_data')

    # Name zusammensetzen
    name = f"{request.user.first_name} {request.user.last_name}"

    # Text aus persönlicher Info (z.B. Qualifikationen, Motivation, etc.)
    pinfo_text = f"{pinfo.background}"  # anpassen je nach Feldern

    # GPT-Funktion aufrufen
    letter_text = generate_application_letter(
        name=name,
        p_info=pinfo_text,
        position=offer.position,
        comp_name=offer.company,
        comp_desc=offer.about_company,
        offer=offer.offer_text
    )

    # Brief speichern
    if letter_text:
        # Hole oder erstelle die Application-Instanz
        letter, created = Application.objects.get_or_create(
            user=request.user,  # Benutzer hinzufügen
            offer=offer
        )
        letter.resume = letter_text  # Setze das Anschreiben
        letter.save()

    # Weiterleitung zur Ansicht des Briefes
    return redirect('job_hunter:view_letter', offer_id=offer.id)


@login_required
def view_letter(request, offer_id):
    # Hole das Angebot und stelle sicher, dass der Benutzer zu diesem Angebot gehört
    offer = get_object_or_404(Offer, id=offer_id, user=request.user)

    # Holen der Application-Instanz für das aktuelle Angebot und den Benutzer
    letter = get_object_or_404(Application, offer=offer, user=request.user)

    # Der tatsächliche Text des Bewerbungsschreibens
    letter_text = letter.resume  # Das Bewerbungsanschreiben (resume) aus der DB

    return render(request, "offers/generated_letter.html", {
        "letter_text": letter_text,
        "offer": offer,
        "letter": letter  # Wir geben das ganze Letter-Objekt weiter, um den Edit-Link zu ermöglichen
    })


class OfferDeleteView(DeleteView):
    model = Offer
    template_name = 'offers/offer_confirm_delete.html'
    context_object_name = 'offer'
    success_url = reverse_lazy('job_hunter:offer_list')

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)


@login_required
def dashboard_view(request):
    user_id = request.user.id
    stats = {}

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                COUNT(o.id) AS total_offers,
                COUNT(CASE WHEN o.response = 1 THEN 1 END) AS responded_offers,
                COUNT(CASE WHEN o.status IS NOT NULL AND o.status != 0 THEN 1 END) AS total_applications,
                COUNT(CASE WHEN o.status = 1 THEN 1 END) AS open_applications,
                COUNT(CASE WHEN o.status = 2 THEN 1 END) AS applied_applications,
                COUNT(CASE WHEN o.status = 3 THEN 1 END) AS rejected_applications,
                COUNT(CASE WHEN o.status = 4 THEN 1 END) AS accepted_applications
            FROM users_customuser u
            LEFT JOIN job_hunter_offer o ON u.id = o.user_id
            WHERE u.id = %s
            GROUP BY u.id;
        """,
            [user_id],
        )

        row = cursor.fetchone()
        if row:
            (
                stats["total_offers"],
                stats["responded_offers"],
                stats["total_applications"],
                stats["open_applications"],
                stats["applied_applications"],
                stats["rejected_applications"],
                stats["accepted_applications"],
            ) = row

    return render(request, "job_hunter/dashboard.html", {"stats": stats})


@login_required
def personal_data_view(request):
    pinfo, created = PInfo.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PInfoForm(request.POST, instance=pinfo)
        if form.is_valid():
            form.save()
            return redirect("job_hunter:personal_data")
    else:
        form = PInfoForm(instance=pinfo)

    return render(request, "job_hunter/personal_data.html", {"form": form})



class OfferListView(ListView):
    model = Offer
    template_name = "offers/offer_list.html"
    context_object_name = "offers"

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)



class OfferDetailView(DetailView):
    model = Offer
    template_name = "offers/offer_detail.html"
    context_object_name = "offer"

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)



class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = "offers/offer_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("job_hunter:offer_list")


class OfferUpdateView(UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = "offers/offer_form.html"

    def get_success_url(self):
        return reverse_lazy("job_hunter:offer_list")
    
    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)


@login_required
def ai_assistant_view(request):
    return render(request, "job_hunter/ai_assistant.html")


@login_required
def search_view(request):
    return render(request, "job_hunter/search.html")
