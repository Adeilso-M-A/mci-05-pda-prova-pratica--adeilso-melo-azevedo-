import { Routes } from '@angular/router';
import { TicketListComponent } from './tickets/ticket-list/ticket-list.component';

export const routes: Routes = [
  { path: '', redirectTo: 'tickets', pathMatch: 'full' },
  { path: 'tickets', component: TicketListComponent },
  { path: '**', redirectTo: 'tickets' },
];
