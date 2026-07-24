"""Exceções customizadas da aplicação de chamados."""

from rest_framework import status
from rest_framework.exceptions import APIException


class TicketNotFound(APIException):
    """Lançada quando um chamado com o ID solicitado não existe."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Chamado não encontrado."
    default_code = "ticket_not_found"
