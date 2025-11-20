/**
 * Unit tests for PercentageFormatPipe
 */
import { PercentageFormatPipe } from './percentage-format.pipe';

describe('PercentageFormatPipe', () => {
  let pipe: PercentageFormatPipe;

  beforeEach(() => {
    pipe = new PercentageFormatPipe();
  });

  it('should create an instance', () => {
    expect(pipe).toBeTruthy();
  });

  describe('Basic formatting', () => {
    it('should format whole numbers', () => {
      expect(pipe.transform(75)).toBe('75%');
    });

    it('should format zero', () => {
      expect(pipe.transform(0)).toBe('0%');
    });

    it('should format 100', () => {
      expect(pipe.transform(100)).toBe('100%');
    });

    it('should round decimals by default', () => {
      expect(pipe.transform(75.5)).toBe('76%');
      expect(pipe.transform(75.4)).toBe('75%');
    });
  });

  describe('Decimal places', () => {
    it('should use default 0 decimal places', () => {
      expect(pipe.transform(42.567)).toBe('43%');
    });

    it('should accept custom decimal places', () => {
      expect(pipe.transform(42.567, 1)).toBe('42.6%');
      expect(pipe.transform(42.567, 2)).toBe('42.57%');
      expect(pipe.transform(42.567, 3)).toBe('42.567%');
    });

    it('should handle whole numbers with decimal places', () => {
      expect(pipe.transform(50, 2)).toBe('50.00%');
    });
  });

  describe('Edge cases', () => {
    it('should handle null', () => {
      expect(pipe.transform(null)).toBe('0%');
    });

    it('should handle undefined', () => {
      expect(pipe.transform(undefined)).toBe('0%');
    });

    it('should handle NaN', () => {
      expect(pipe.transform(NaN)).toBe('0%');
    });

    it('should handle negative values', () => {
      expect(pipe.transform(-10)).toBe('-10%');
    });

    it('should handle values over 100', () => {
      expect(pipe.transform(125)).toBe('125%');
    });

    it('should handle very small decimals', () => {
      expect(pipe.transform(0.5, 1)).toBe('0.5%');
    });
  });
});
