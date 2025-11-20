/**
 * Customer model representing a TelcoX customer
 */
export interface Customer {
  id: number;
  customer_code: string;
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
  created_at: string;
  updated_at: string;
}
