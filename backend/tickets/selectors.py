"""Selectors da aplicação de chamados — encapsula as queries ao banco."""

from django.db.models import QuerySet

from tickets.models import Ticket


def get_all_tickets(status: str | None = None) -> QuerySet[Ticket]:
    """Retorna todos os chamados, com filtro opcional por status.

    Args:
        status: Se informado ('open' ou 'closed'), filtra por status.

    Returns:
        QuerySet com os chamados encontrados.
    """
    queryset = Ticket.objects.all()
    if status:
        queryset = queryset.filter(status=status)
    return queryset


def get_ticket_by_id(ticket_id: int) -> Ticket:
    """Busca um chamado pelo ID.

    Args:
        ticket_id: ID do chamado.

    Returns:
        Instância do chamado encontrado.

    Raises:
        Ticket.DoesNotExist: Se nenhum chamado com este ID existir.
    """
    return Ticket.objects.get(pk=ticket_id)
