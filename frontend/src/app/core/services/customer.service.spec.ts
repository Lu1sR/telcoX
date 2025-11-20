/**
 * Unit tests for CustomerService
 */
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { CustomerService } from './customer.service';
import { ApiService } from './api.service';
import { Customer } from '../models';

describe('CustomerService', () => {
  let service: CustomerService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        CustomerService,
        ApiService
      ]
    });
    
    service = TestBed.inject(CustomerService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getCustomers', () => {
    const mockCustomers: Customer[] = [
      {
        id: 1,
        customer_code: 'CUST-001',
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        phone_number: '+1234567890',
        created_at: '2025-01-01T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z'
      },
      {
        id: 2,
        customer_code: 'CUST-002',
        first_name: 'Jane',
        last_name: 'Smith',
        email: 'jane.smith@example.com',
        created_at: '2025-01-01T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z'
      }
    ];

    it('should call correct API endpoint', () => {
      service.getCustomers().subscribe();

      const req = httpMock.expectOne('http://localhost:8010/api/customers/');
      expect(req.request.method).toBe('GET');
      req.flush(mockCustomers);
    });

    it('should return list of customers', (done) => {
      service.getCustomers().subscribe(customers => {
        expect(customers.length).toBe(2);
        expect(customers[0].customer_code).toBe('CUST-001');
        expect(customers[1].customer_code).toBe('CUST-002');
        done();
      });

      const req = httpMock.expectOne('http://localhost:8010/api/customers/');
      req.flush(mockCustomers);
    });
  });

  describe('getCustomer', () => {
    const mockCustomer: Customer = {
      id: 1,
      customer_code: 'CUST-001',
      first_name: 'John',
      last_name: 'Doe',
      email: 'john.doe@example.com',
      phone_number: '+1234567890',
      created_at: '2025-01-01T00:00:00Z',
      updated_at: '2025-01-01T00:00:00Z'
    };

    it('should call correct API endpoint with ID', () => {
      service.getCustomer(1).subscribe();

      const req = httpMock.expectOne('http://localhost:8010/api/customers/1/');
      expect(req.request.method).toBe('GET');
      req.flush(mockCustomer);
    });

    it('should return single customer', (done) => {
      service.getCustomer(1).subscribe(customer => {
        expect(customer.id).toBe(1);
        expect(customer.customer_code).toBe('CUST-001');
        done();
      });

      const req = httpMock.expectOne('http://localhost:8010/api/customers/1/');
      req.flush(mockCustomer);
    });

    it('should handle 404 error', (done) => {
      service.getCustomer(999).subscribe(
        () => fail('should have failed with 404'),
        (error) => {
          expect(error.status).toBe(404);
          done();
        }
      );

      const req = httpMock.expectOne('http://localhost:8010/api/customers/999/');
      req.flush({ detail: 'Not found' }, { status: 404, statusText: 'Not Found' });
    });
  });
});
