/**
 * Usage Card Component
 * Reusable card for displaying usage metrics with progress bar
 */
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-usage-card',
  templateUrl: './usage-card.component.html',
  styleUrls: ['./usage-card.component.scss']
})
export class UsageCardComponent {
  @Input() title = '';
  @Input() used: number | string = 0;
  @Input() total: number | string | null = null;
  @Input() unit = '';
  @Input() percentage: number | null = null;
  @Input() icon = '📊';
  @Input() isUnlimited = false;

  /**
   * Get percentage for progress bar
   * If null, calculate from used/total
   */
  get progressPercentage(): number {
    if (this.isUnlimited) return 0;
    
    if (this.percentage !== null && this.percentage !== undefined) {
      return Math.min(this.percentage, 100);
    }

    // Calculate from used/total if percentage not provided
    const usedNum = Number(this.used);
    const totalNum = Number(this.total);
    
    if (totalNum && totalNum > 0) {
      return Math.min((usedNum / totalNum) * 100, 100);
    }

    return 0;
  }

  /**
   * Get progress bar color based on percentage
   */
  get progressColor(): string {
    if (this.isUnlimited) return '#95a5a6';
    
    const percent = this.progressPercentage;
    
    if (percent >= 90) return '#e74c3c';  // Red
    if (percent >= 75) return '#e67e22';  // Orange
    if (percent >= 50) return '#f39c12';  // Yellow
    return '#27ae60';  // Green
  }

  /**
   * Format display text for used/total
   */
  get displayText(): string {
    if (this.isUnlimited) {
      return `${this.formatNumber(this.used)} ${this.unit} (Unlimited)`;
    }

    if (this.total === null || this.total === undefined) {
      return `${this.formatNumber(this.used)} ${this.unit}`;
    }

    return `${this.formatNumber(this.used)} / ${this.formatNumber(this.total)} ${this.unit}`;
  }

  /**
   * Format number with commas
   */
  private formatNumber(value: number | string): string {
    const num = Number(value);
    if (isNaN(num)) return String(value);
    return num.toLocaleString('en-US', { maximumFractionDigits: 2 });
  }
}
