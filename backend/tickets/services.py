"""Services da aplicação de chamados — lógica de negócio."""

import structlog

from tickets.exceptions import TicketNotFound
from tickets.models import Ticket
from tickets.selectors import get_ticket_by_id

logger = structlog.get_logger(__name__)


def create_ticket(title: str, description: str) -> Ticket:
    """Abre um novo chamado.

    Args:
        title: Título do chamado.
        description: Descrição detalhada.

    Returns:
        Instância do chamado criado (status inicial: open).
    """
    ticket = Ticket.objects.create(title=title, description=description)
    logger.info("ticket_created", ticket_id=ticket.pk, title=ticket.title)
    return ticket


def update_ticket_status(ticket_id: int, status: str) -> Ticket:
    """Atualiza o status de um chamado.

    Args:
        ticket_id: ID do chamado.
        status: Novo status ('open' ou 'closed').

    Returns:
        Instância do chamado atualizado.

    Raises:
        TicketNotFound: Se o chamado não existir.
    """
    try:
        ticket = get_ticket_by_id(ticket_id)
    except Ticket.DoesNotExist:
        raise TicketNotFound()

    ticket.status = status
    ticket.save(update_fields=["status"])

    logger.info("ticket_status_updated", ticket_id=ticket.pk, new_status=status)
    return ticket


def delete_ticket(ticket_id: int) -> None:
    """Remove um chamado do banco de dados.

    Args:
        ticket_id: ID do chamado.

    Raises:
        TicketNotFound: Se o chamado não existir.
    """
    try:
        ticket = get_ticket_by_id(ticket_id)
    except Ticket.DoesNotExist:
        raise TicketNotFound()

    logger.info("ticket_deleted", ticket_id=ticket.pk, title=ticket.title)
    ticket.delete()
