/**
 * Formulário de abertura de chamado.
 */

import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TicketService } from '../ticket.service';
import { TicketFormData } from '../ticket.model';

@Component({
  selector: 'app-ticket-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './ticket-form.component.html',
})
export class TicketFormComponent {
  @Output() ticketCreated = new EventEmitter<void>();

  formData: TicketFormData = { title: '', description: '' };
  isSubmitting: boolean = false;
  errorMessage: string = '';

  constructor(private ticketService: TicketService) {}

  onSubmit(): void {
    this.isSubmitting = true;
    this.errorMessage = '';

    this.ticketService.createTicket(this.formData).subscribe({
      next: () => {
        this.ticketCreated.emit();
        this.formData = { title: '', description: '' };
        this.isSubmitting = false;
      },
      error: () => {
        this.errorMessage = 'Erro ao abrir o chamado.';
        this.isSubmitting = false;
      },
    });
  }
}
