"""Serializers da aplicação de chamados."""

from rest_framework import serializers

from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Serializer completo do chamado — usado para listagem e criação."""

    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "status", "created_at"]
        read_only_fields = ["id", "created_at"]


class TicketStatusSerializer(serializers.Serializer):
    """Serializer para atualizar apenas o status de um chamado."""

    status = serializers.ChoiceField(choices=Ticket.Status.choices)
