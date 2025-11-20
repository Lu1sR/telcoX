/**
 * Unit tests for SafeNumberPipe
 */
import { SafeNumberPipe } from './safe-number.pipe';

describe('SafeNumberPipe', () => {
  let pipe: SafeNumberPipe;

  beforeEach(() => {
    pipe = new SafeNumberPipe();
  });

  it('should create an instance', () => {
    expect(pipe).toBeTruthy();
  });

  describe('Basic formatting', () => {
    it('should format integers with commas', () => {
      expect(pipe.transform(1000)).toBe('1,000');
      expect(pipe.transform(1000000)).toBe('1,000,000');
    });

    it('should format small numbers without commas', () => {
      expect(pipe.transform(100)).toBe('100');
      expect(pipe.transform(999)).toBe('999');
    });

    it('should format zero', () => {
      expect(pipe.transform(0)).toBe('0');
    });
  });

  describe('Decimal places', () => {
    it('should use default 0 decimal places', () => {
      expect(pipe.transform(1234.567)).toBe('1,235');
    });

    it('should accept custom decimal places', () => {
      expect(pipe.transform(1234.567, 1)).toBe('1,234.6');
      expect(pipe.transform(1234.567, 2)).toBe('1,234.57');
      expect(pipe.transform(1234.567, 3)).toBe('1,234.567');
    });

    it('should pad decimals when needed', () => {
      expect(pipe.transform(1000, 2)).toBe('1,000.00');
      expect(pipe.transform(42.5, 2)).toBe('42.50');
    });
  });

  describe('String input', () => {
    it('should handle string numbers', () => {
      expect(pipe.transform('1500000')).toBe('1,500,000');
    });

    it('should handle string decimals', () => {
      expect(pipe.transform('1234.56', 2)).toBe('1,234.56');
    });

    it('should handle invalid strings', () => {
      expect(pipe.transform('invalid')).toBe('0');
    });
  });

  describe('Edge cases', () => {
    it('should handle null', () => {
      expect(pipe.transform(null)).toBe('0');
    });

    it('should handle undefined', () => {
      expect(pipe.transform(undefined)).toBe('0');
    });

    it('should handle NaN', () => {
      expect(pipe.transform(NaN)).toBe('0');
    });

    it('should handle negative values', () => {
      expect(pipe.transform(-1000)).toBe('-1,000');
      expect(pipe.transform(-1234.56, 2)).toBe('-1,234.56');
    });

    it('should handle very large numbers', () => {
      expect(pipe.transform(999999999)).toBe('999,999,999');
    });
  });
});
