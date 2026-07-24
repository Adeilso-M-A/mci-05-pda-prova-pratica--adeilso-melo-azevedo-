"""Views da aplicação de chamados — orquestradores finos."""

import structlog
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.selectors import get_all_tickets
from tickets.serializers import TicketSerializer, TicketStatusSerializer
from tickets.services import create_ticket, delete_ticket, update_ticket_status

logger = structlog.get_logger(__name__)


class TicketListView(APIView):
    """Listagem e criação de chamados.

    GET  /api/tickets/           → lista todos os chamados
    GET  /api/tickets/?status=open → filtra por status
    POST /api/tickets/           → abre um novo chamado
    """

    def get(self, request: Request) -> Response:
        """Lista os chamados, com filtro opcional por status."""
        ticket_status = request.query_params.get("status")
        tickets = get_all_tickets(status=ticket_status)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Abre um novo chamado."""
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = create_ticket(
            title=serializer.validated_data["title"],
            description=serializer.validated_data["description"],
        )
        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


class TicketDetailView(APIView):
    """Remoção de um chamado específico.

    DELETE /api/tickets/<id>/ → remove o chamado
    """

    def delete(self, request: Request, pk: int) -> Response:
        """Remove um chamado."""
        delete_ticket(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TicketStatusView(APIView):
    """Atualização do status de um chamado.

    PATCH /api/tickets/<id>/status/ → atualiza apenas o status
    """

    def patch(self, request: Request, pk: int) -> Response:
        """Atualiza o status de um chamado (open/closed)."""
        serializer = TicketStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = update_ticket_status(pk, serializer.validated_data["status"])
        return Response(TicketSerializer(ticket).data)
