"""
Roteamento de URLs da aplicação de chamados.

GET    /api/tickets/              → lista chamados
GET    /api/tickets/?status=open  → filtra por status
POST   /api/tickets/              → abre chamado
DELETE /api/tickets/<id>/         → remove chamado
PATCH  /api/tickets/<id>/status/  → atualiza status
"""

from django.urls import path

from tickets.views import TicketDetailView, TicketListView, TicketStatusView

urlpatterns = [
    path("tickets/", TicketListView.as_view(), name="ticket-list"),
    path("tickets/<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    path("tickets/<int:pk>/status/", TicketStatusView.as_view(), name="ticket-status"),
]
