from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PInfo
from .forms import PInfoForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import connection
from django.urls import reverse_lazy
from .models import Offer
from .forms import OfferForm

@login_required
def dashboard_view(request):
    user_id = request.user.id
    stats = {}

    with connection.cursor() as cursor:
        cursor.execute("""
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
        """, [user_id])
        
        row = cursor.fetchone()
        if row:
            (stats["total_offers"], stats["responded_offers"], stats["total_applications"],
             stats["open_applications"], stats["applied_applications"],
             stats["rejected_applications"], stats["accepted_applications"]) = row

    return render(request, "job_hunter/dashboard.html", {"stats": stats})


@login_required
def personal_data_view(request):
    pinfo, created = PInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PInfoForm(request.POST, instance=pinfo)
        if form.is_valid():
            form.save()
            return redirect('job_hunter:personal_data')
    else:
        form = PInfoForm(instance=pinfo)

    return render(request, 'job_hunter/personal_data.html', {'form': form})


class OfferListView(ListView):
    model = Offer
    template_name = 'offers/offer_list.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)

class OfferDetailView(DetailView):
    model = Offer
    template_name = 'offers/offer_detail.html'
    context_object_name = 'offer'

class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offers/offer_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('offer_list')

class OfferUpdateView(UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offers/offer_form.html'

    def get_success_url(self):
        return reverse_lazy('offer_list')


@login_required
def ai_assistant_view(request):
    return render(request, "job_hunter/ai_assistant.html")


@login_required
def search_view(request):
    return render(request, "job_hunter/search.html")

