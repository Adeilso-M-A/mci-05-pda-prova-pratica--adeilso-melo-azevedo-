"""Testes de integração da API de chamados."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tickets.models import Ticket


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def open_ticket() -> Ticket:
    return Ticket.objects.create(title="Erro no login", description="Não consigo acessar.")


@pytest.fixture
def closed_ticket() -> Ticket:
    return Ticket.objects.create(
        title="Lentidão no sistema", description="Sistema lento.", status="closed"
    )


@pytest.mark.django_db
class TestTicketList:
    """Testes do endpoint GET/POST /api/tickets/"""

    def test_list_empty(self, api_client: APIClient) -> None:
        response = api_client.get(reverse("ticket-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_list_returns_tickets(
        self, api_client: APIClient, open_ticket: Ticket
    ) -> None:
        response = api_client.get(reverse("ticket-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_filter_by_status_open(
        self, api_client: APIClient, open_ticket: Ticket, closed_ticket: Ticket
    ) -> None:
        response = api_client.get(reverse("ticket-list"), {"status": "open"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["status"] == "open"

    def test_filter_by_status_closed(
        self, api_client: APIClient, open_ticket: Ticket, closed_ticket: Ticket
    ) -> None:
        response = api_client.get(reverse("ticket-list"), {"status": "closed"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["status"] == "closed"

    def test_create_ticket_returns_201(self, api_client: APIClient) -> None:
        payload = {"title": "Impressora não funciona", "description": "Erro 0x0001"}
        response = api_client.post(reverse("ticket-list"), payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "open"

    def test_create_ticket_missing_description_returns_400(
        self, api_client: APIClient
    ) -> None:
        response = api_client.post(
            reverse("ticket-list"), {"title": "Sem descrição"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTicketStatus:
    """Testes do endpoint PATCH /api/tickets/<id>/status/"""

    def test_close_ticket(self, api_client: APIClient, open_ticket: Ticket) -> None:
        url = reverse("ticket-status", kwargs={"pk": open_ticket.pk})
        response = api_client.patch(url, {"status": "closed"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "closed"

    def test_reopen_ticket(self, api_client: APIClient, closed_ticket: Ticket) -> None:
        url = reverse("ticket-status", kwargs={"pk": closed_ticket.pk})
        response = api_client.patch(url, {"status": "open"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "open"

    def test_invalid_status_returns_400(
        self, api_client: APIClient, open_ticket: Ticket
    ) -> None:
        url = reverse("ticket-status", kwargs={"pk": open_ticket.pk})
        response = api_client.patch(url, {"status": "pendente"}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_nonexistent_ticket_returns_404(self, api_client: APIClient) -> None:
        url = reverse("ticket-status", kwargs={"pk": 99999})
        response = api_client.patch(url, {"status": "closed"}, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTicketDelete:
    """Testes do endpoint DELETE /api/tickets/<id>/"""

    def test_delete_ticket_returns_204(
        self, api_client: APIClient, open_ticket: Ticket
    ) -> None:
        url = reverse("ticket-detail", kwargs={"pk": open_ticket.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Ticket.objects.count() == 0

    def test_delete_nonexistent_returns_404(self, api_client: APIClient) -> None:
        url = reverse("ticket-detail", kwargs={"pk": 99999})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
