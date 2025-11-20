/**
 * Safe Number Pipe
 * Safely converts value to number and formats with commas
 */
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'safeNumber'
})
export class SafeNumberPipe implements PipeTransform {
  transform(value: number | string | null | undefined, decimalPlaces: number = 0): string {
    if (value === null || value === undefined) {
      return '0';
    }

    const num = Number(value);
    
    if (isNaN(num)) {
      return '0';
    }

    return num.toLocaleString('en-US', {
      minimumFractionDigits: decimalPlaces,
      maximumFractionDigits: decimalPlaces
    });
  }
}
