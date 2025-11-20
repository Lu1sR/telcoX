/**
 * Account model representing a customer's billing account
 */
export interface Account {
  id: number;
  balance: string;
  currency: string;
  status: 'ACTIVE' | 'SUSPENDED' | 'CLOSED';
  created_at: string;
  updated_at: string;
}
