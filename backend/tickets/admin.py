"""Configuração do Django Admin para o modelo Ticket."""

from django.contrib import admin

from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
