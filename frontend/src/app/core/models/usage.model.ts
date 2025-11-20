/**
 * Usage record model representing customer consumption data
 */
export interface UsageRecord {
  id: number;
  billing_period_start: string;
  billing_period_end: string;
  data_used_mb: string;
  data_limit_mb: string | null;
  data_used_percentage: number | null;
  minutes_used: number;
  minutes_limit: number | null;
  minutes_used_percentage: number | null;
  sms_used: number;
  sms_limit: number | null;
  sms_used_percentage: number | null;
  created_at: string;
  updated_at: string;
}
