/**
 * Unit tests for DataFormatPipe
 */
import { DataFormatPipe } from './data-format.pipe';

describe('DataFormatPipe', () => {
  let pipe: DataFormatPipe;

  beforeEach(() => {
    pipe = new DataFormatPipe();
  });

  it('should create an instance', () => {
    expect(pipe).toBeTruthy();
  });

  describe('MB conversions', () => {
    it('should format small values as MB', () => {
      expect(pipe.transform(500)).toBe('500.00 MB');
    });

    it('should format 0 as MB', () => {
      expect(pipe.transform(0)).toBe('0.00 MB');
    });

    it('should format decimal MB values', () => {
      expect(pipe.transform(250.5)).toBe('250.50 MB');
    });
  });

  describe('GB conversions', () => {
    it('should convert 1024 MB to GB', () => {
      expect(pipe.transform(1024)).toBe('1.00 GB');
    });

    it('should convert 1500 MB to GB', () => {
      expect(pipe.transform(1500)).toBe('1.46 GB');
    });

    it('should convert 2048 MB to GB', () => {
      expect(pipe.transform(2048)).toBe('2.00 GB');
    });
  });

  describe('TB conversions', () => {
    it('should convert large values to TB', () => {
      const oneTB = 1024 * 1024; // 1,048,576 MB
      expect(pipe.transform(oneTB)).toBe('1.00 TB');
    });

    it('should convert 1.5 TB correctly', () => {
      const oneAndHalfTB = 1024 * 1024 * 1.5;
      expect(pipe.transform(oneAndHalfTB)).toBe('1.50 TB');
    });
  });

  describe('Decimal places', () => {
    it('should use default 2 decimal places', () => {
      expect(pipe.transform(1500)).toBe('1.46 GB');
    });

    it('should accept custom decimal places', () => {
      expect(pipe.transform(1500, 1)).toBe('1.5 GB');
      expect(pipe.transform(1500, 3)).toBe('1.465 GB');
      expect(pipe.transform(1500, 0)).toBe('1 GB');
    });
  });

  describe('Edge cases', () => {
    it('should handle null', () => {
      expect(pipe.transform(null)).toBe('0 MB');
    });

    it('should handle undefined', () => {
      expect(pipe.transform(undefined)).toBe('0 MB');
    });

    it('should handle string numbers', () => {
      expect(pipe.transform('1500')).toBe('1.46 GB');
    });

    it('should handle invalid strings', () => {
      expect(pipe.transform('invalid')).toBe('0 MB');
    });

    it('should handle negative values', () => {
      expect(pipe.transform(-100)).toBe('-100.00 MB');
    });
  });
});
