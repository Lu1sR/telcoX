/**
 * Usage Component (Container)
 * Displays customer usage information including data and minutes usage
 */
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { UsageService } from '@core/services/usage.service';
import { LoadingService } from '@core/services/loading.service';
import { CustomerUsageOverview } from '@core/models';

@Component({
  selector: 'app-usage',
  templateUrl: './usage.component.html',
  styleUrls: ['./usage.component.scss']
})
export class UsageComponent implements OnInit, OnDestroy {
  // State management
  customerData: CustomerUsageOverview | null = null;
  isLoading = false;
  error: string | null = null;
  isEmpty = false;

  // For now, use a fixed customer ID. Can be parameterized later via route params
  private readonly customerId = 1;
  private destroy$ = new Subject<void>();

  constructor(
    private usageService: UsageService,
    public loadingService: LoadingService
  ) {}

  ngOnInit(): void {
    this.loadUsageData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Load customer usage data from API
   */
  loadUsageData(): void {
    this.isLoading = true;
    this.error = null;
    this.isEmpty = false;

    this.usageService.getCustomerUsageOverview(this.customerId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.customerData = data;
          this.isLoading = false;

          // Check if we have usage data
          if (!data.usage) {
            this.isEmpty = true;
          }
        },
        error: (err) => {
          this.isLoading = false;
          this.error = err.message || 'Failed to load usage data. Please try again.';
          console.error('Error loading usage data:', err);
        }
      });
  }

  /**
   * Retry loading data
   */
  retry(): void {
    this.loadUsageData();
  }

  /**
   * Get customer full name
   */
  get customerName(): string {
    if (!this.customerData?.customer) return '';
    const { first_name, last_name } = this.customerData.customer;
    return `${first_name} ${last_name}`;
  }

  /**
   * Get account balance formatted
   */
  get accountBalance(): string {
    if (!this.customerData?.account) return '0.00';
    return this.customerData.account.balance;
  }

  /**
   * Get account status with styling class
   */
  get accountStatus(): string {
    return this.customerData?.account?.status || 'UNKNOWN';
  }

  get accountStatusClass(): string {
    const status = this.accountStatus;
    switch (status) {
      case 'ACTIVE':
        return 'status-active';
      case 'SUSPENDED':
        return 'status-suspended';
      case 'CLOSED':
        return 'status-closed';
      default:
        return 'status-unknown';
    }
  }
}
