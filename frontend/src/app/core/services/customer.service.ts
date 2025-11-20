/**
 * Customer service for managing customer-related API calls
 */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Customer } from '@core/models';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  private readonly endpoint = '/customers';

  constructor(private apiService: ApiService) {}

  /**
   * Get all customers
   * GET /api/customers/
   */
  getCustomers(): Observable<Customer[]> {
    return this.apiService.get<Customer[]>(`${this.endpoint}/`);
  }

  /**
   * Get a single customer by ID
   * GET /api/customers/{id}/
   */
  getCustomer(id: number): Observable<Customer> {
    return this.apiService.get<Customer>(`${this.endpoint}/${id}/`);
  }

  /**
   * Search customers by query
   * GET /api/customers/?search={query}
   */
  searchCustomers(query: string): Observable<Customer[]> {
    return this.apiService.get<Customer[]>(`${this.endpoint}/?search=${query}`);
  }
}
