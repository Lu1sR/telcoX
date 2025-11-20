/**
 * Percentage Format Pipe
 * Formats a number as a percentage with proper rounding
 */
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'percentageFormat'
})
export class PercentageFormatPipe implements PipeTransform {
  transform(value: number | null | undefined, decimalPlaces: number = 0): string {
    if (value === null || value === undefined) {
      return '0%';
    }

    const num = Number(value);
    
    if (isNaN(num)) {
      return '0%';
    }

    return `${num.toFixed(decimalPlaces)}%`;
  }
}
