/**
 * Usage service for managing usage-related API calls
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { CustomerUsageOverview } from '@core/models';

@Injectable({
  providedIn: 'root'
})
export class UsageService {
  constructor(private apiService: ApiService) {}

  /**
   * Get complete usage overview for a customer
   * Returns customer info, account balance, and current usage data
   * GET /api/customers/{id}/usage/
   * 
   * This is the main endpoint for the "My Usage" screen
   */
  getCustomerUsageOverview(customerId: number): Observable<CustomerUsageOverview> {
    return this.apiService.get<CustomerUsageOverview>(`/customers/${customerId}/usage/`);
  }
}
