/**
 * Interface que define o formato de um chamado na aplicação Angular.
 */

export interface Ticket {
  id: number;
  title: string;
  description: string;
  status: 'open' | 'closed';
  created_at: string;
}

export interface TicketFormData {
  title: string;
  description: string;
}
