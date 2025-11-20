/**
 * Data Format Pipe
 * Converts MB to human-readable format (MB, GB, TB)
 */
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dataFormat'
})
export class DataFormatPipe implements PipeTransform {
  transform(value: number | string | null | undefined, decimalPlaces: number = 2): string {
    if (value === null || value === undefined) {
      return '0 MB';
    }

    const mb = Number(value);
    
    if (isNaN(mb)) {
      return '0 MB';
    }

    // Convert to appropriate unit
    if (mb >= 1024 * 1024) {
      // TB
      return `${(mb / (1024 * 1024)).toFixed(decimalPlaces)} TB`;
    } else if (mb >= 1024) {
      // GB
      return `${(mb / 1024).toFixed(decimalPlaces)} GB`;
    } else {
      // MB
      return `${mb.toFixed(decimalPlaces)} MB`;
    }
  }
}
