/**
 * Componente de listagem de chamados.
 * Exibe os chamados separados em duas seções: Abertos e Fechados.
 */

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Ticket } from '../ticket.model';
import { TicketService } from '../ticket.service';
import { TicketFormComponent } from '../ticket-form/ticket-form.component';

@Component({
  selector: 'app-ticket-list',
  standalone: true,
  imports: [CommonModule, TicketFormComponent],
  templateUrl: './ticket-list.component.html',
})
export class TicketListComponent implements OnInit {
  // Listas separadas por status
  openTickets: Ticket[] = [];
  closedTickets: Ticket[] = [];
  errorMessage: string = '';

  constructor(private ticketService: TicketService) {}

  ngOnInit(): void {
    this.loadTickets();
  }

  loadTickets(): void {
    this.errorMessage = '';
    this.ticketService.getTickets().subscribe({
      next: (tickets) => {
        // Separa os chamados por status
        this.openTickets = tickets.filter((t) => t.status === 'open');
        this.closedTickets = tickets.filter((t) => t.status === 'closed');
      },
      error: () => {
        this.errorMessage = 'Erro ao carregar chamados.';
      },
    });
  }

  closeTicket(ticket: Ticket): void {
    this.ticketService.updateStatus(ticket.id, 'closed').subscribe({
      next: () => this.loadTickets(),
      error: () => (this.errorMessage = 'Erro ao fechar o chamado.'),
    });
  }

  reopenTicket(ticket: Ticket): void {
    this.ticketService.updateStatus(ticket.id, 'open').subscribe({
      next: () => this.loadTickets(),
      error: () => (this.errorMessage = 'Erro ao reabrir o chamado.'),
    });
  }

  deleteTicket(ticket: Ticket): void {
    if (!confirm(`Remover o chamado "${ticket.title}"?`)) return;
    this.ticketService.deleteTicket(ticket.id).subscribe({
      next: () => this.loadTickets(),
      error: () => (this.errorMessage = 'Erro ao remover o chamado.'),
    });
  }

  onTicketCreated(): void {
    this.loadTickets();
  }
}
