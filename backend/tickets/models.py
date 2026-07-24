"""
Model do Gerenciador de Chamados.

Este é o modelo da aplicação usada na prova final.
Os alunos receberão apenas o backend e o frontend.
Precisarão criar toda a infraestrutura Docker do zero.
"""

from django.db import models


class Ticket(models.Model):
    """Representa um chamado de suporte.

    Attributes:
        title: Título resumido do chamado.
        description: Descrição detalhada do problema.
        status: Status atual — 'open' (aberto) ou 'closed' (fechado).
        created_at: Data e hora de abertura, preenchida automaticamente.
    """

    class Status(models.TextChoices):
        """Opções válidas para o campo status."""

        OPEN = "open", "Aberto"
        CLOSED = "closed", "Fechado"

    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Aberto em")

    class Meta:
        db_table = "tickets"
        ordering = ["-created_at"]
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"

    def __str__(self) -> str:
        return f"[{self.get_status_display()}] {self.title}"
