/**
 * Combined model for customer usage overview
 * This represents the response from GET /api/customers/{id}/usage/
 */
import { Customer } from './customer.model';
import { Account } from './account.model';
import { UsageRecord } from './usage.model';

export interface CustomerUsageOverview {
  customer: Customer;
  account: Account | null;
  usage: UsageRecord | null;
}
