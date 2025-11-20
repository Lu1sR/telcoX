/**
 * Unit tests for UsageService
 */
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UsageService } from './usage.service';
import { ApiService } from './api.service';
import { CustomerUsageOverview } from '../models';

describe('UsageService', () => {
  let service: UsageService;
  let httpMock: HttpTestingController;
  let apiService: ApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        UsageService,
        ApiService
      ]
    });
    
    service = TestBed.inject(UsageService);
    httpMock = TestBed.inject(HttpTestingController);
    apiService = TestBed.inject(ApiService);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getCustomerUsageOverview', () => {
    const customerId = 1;
    const mockResponse: CustomerUsageOverview = {
      customer: {
        id: 1,
        customer_code: 'CUST-001',
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        phone_number: '+1234567890',
        created_at: '2025-01-01T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z'
      },
      account: {
        id: 1,
        balance: '1250.00',
        currency: 'USD',
        status: 'ACTIVE',
        created_at: '2025-01-01T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z'
      },
      usage: {
        id: 1,
        billing_period_start: '2025-01-01',
        billing_period_end: '2025-01-31',
        data_used_mb: '1500.00',
        data_limit_mb: '2000.00',
        data_used_percentage: 75.0,
        minutes_used: 250,
        minutes_limit: 500,
        minutes_used_percentage: 50.0,
        sms_used: 50,
        sms_limit: 100,
        sms_used_percentage: 50.0,
        created_at: '2025-01-01T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z'
      }
    };

    it('should call correct API endpoint', () => {
      service.getCustomerUsageOverview(customerId).subscribe();

      const req = httpMock.expectOne(`http://localhost:8010/api/customers/${customerId}/usage/`);
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });

    it('should return CustomerUsageOverview on success', (done) => {
      service.getCustomerUsageOverview(customerId).subscribe(data => {
        expect(data).toEqual(mockResponse);
        expect(data.customer.customer_code).toBe('CUST-001');
        expect(data.account?.status).toBe('ACTIVE');
        expect(data.usage?.data_used_percentage).toBe(75.0);
        done();
      });

      const req = httpMock.expectOne(`http://localhost:8010/api/customers/${customerId}/usage/`);
      req.flush(mockResponse);
    });

    it('should handle HTTP error responses', (done) => {
      const errorMessage = 'Customer not found';

      service.getCustomerUsageOverview(customerId).subscribe(
        () => fail('should have failed with 404 error'),
        (error) => {
          expect(error.status).toBe(404);
          done();
        }
      );

      const req = httpMock.expectOne(`http://localhost:8010/api/customers/${customerId}/usage/`);
      req.flush({ detail: errorMessage }, { status: 404, statusText: 'Not Found' });
    });

    it('should handle network errors', (done) => {
      service.getCustomerUsageOverview(customerId).subscribe(
        () => fail('should have failed with network error'),
        (error) => {
          expect(error).toBeTruthy();
          done();
        }
      );

      const req = httpMock.expectOne(`http://localhost:8010/api/customers/${customerId}/usage/`);
      req.error(new ProgressEvent('Network error'));
    });
  });
});
