/**
 * Serviço de comunicação com a API de chamados.
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ticket, TicketFormData } from './ticket.model';

const API_URL = '/api/tickets/';

@Injectable({ providedIn: 'root' })
export class TicketService {
  constructor(private http: HttpClient) {}

  /** Busca chamados, com filtro opcional por status. */
  getTickets(status?: 'open' | 'closed'): Observable<Ticket[]> {
    let params = new HttpParams();
    if (status) params = params.set('status', status);
    return this.http.get<Ticket[]>(API_URL, { params });
  }

  /** Abre um novo chamado. */
  createTicket(data: TicketFormData): Observable<Ticket> {
    return this.http.post<Ticket>(API_URL, data);
  }

  /**
   * Atualiza o status de um chamado.
   *
   * @param id - ID do chamado
   * @param status - 'open' ou 'closed'
   */
  updateStatus(id: number, status: 'open' | 'closed'): Observable<Ticket> {
    return this.http.patch<Ticket>(`${API_URL}${id}/status/`, { status });
  }

  /** Remove um chamado. */
  deleteTicket(id: number): Observable<void> {
    return this.http.delete<void>(`${API_URL}${id}/`);
  }
}
