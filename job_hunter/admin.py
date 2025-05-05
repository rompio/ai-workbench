from django.contrib import admin
from .models import PInfo, Offer, Application, ChatLog
from django.contrib.auth import get_user_model


class PInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'background')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')
    list_filter = ('user',)  # Hier kannst du nach Benutzern filtern

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Filtere die PInfo nach dem eingeloggten Benutzer
        if request.user.is_superuser:
            return queryset  # Admin kann alle sehen
        return queryset.filter(user=request.user)  # Filtere nach dem aktuellen Benutzer

class OfferAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'status', 'user')
    search_fields = ('position', 'company', 'user__username')
    list_filter = ('status', 'user')  # Hier kannst du nach Benutzern und Status filtern

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Filtere nach dem eingeloggten Benutzer
        if request.user.is_superuser:
            return queryset  # Admin kann alle sehen
        return queryset.filter(user=request.user)  # Filtere nach dem aktuellen Benutzer

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'offer', 'submitted_at', 'resume')
    search_fields = ('user__username', 'offer__position', 'resume')
    list_filter = ('user', 'offer')  # Hier kannst du nach Benutzer und Angebot filtern

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Filtere nach dem eingeloggten Benutzer
        if request.user.is_superuser:
            return queryset  # Admin kann alle sehen
        return queryset.filter(user=request.user)  # Filtere nach dem aktuellen Benutzer

class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'user_input', 'assistant_response')
    search_fields = ('user__username', 'user_input', 'assistant_response')
    list_filter = ('user',)  # Hier kannst du nach Benutzern filtern

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Filtere nach dem eingeloggten Benutzer
        if request.user.is_superuser:
            return queryset  # Admin kann alle sehen
        return queryset.filter(user=request.user)  # Filtere nach dem aktuellen Benutzer


admin.site.register(PInfo, PInfoAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ChatLog, ChatLogAdmin)
