"""
Error Handling Integration Tests.

These tests verify the system handles errors gracefully across the entire stack.
Tests cover API error responses, database errors, and edge cases.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from django.test import Client
from django.db import connection
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord


@pytest.mark.integration
class TestErrorHandlingIntegration:
    """Test error handling with real environment."""
    
    def test_api_404_for_nonexistent_customer(self, db):
        """
        Test API returns 404 for non-existent customer.
        
        Verifies:
        - 404 status code returned
        - Error response format is correct
        - No server error (500)
        """
        client = Client()
        response = client.get('/api/customers/999999/')
        
        assert response.status_code == 404
        data = response.json()
        assert 'detail' in data or 'error' in data
    
    def test_api_404_for_nonexistent_customer_usage(self, db):
        """
        Test usage endpoint returns 404 for non-existent customer.
        
        Verifies:
        - Service returns None for missing customer
        - View handles None and returns 404
        """
        client = Client()
        response = client.get('/api/customers/999999/usage/')
        
        assert response.status_code == 404
    
    def test_api_handles_invalid_customer_id_format(self, db):
        """
        Test API handles invalid ID format gracefully.
        
        Verifies:
        - Non-numeric IDs return proper error
        - No server crash
        """
        client = Client()
        response = client.get('/api/customers/invalid-id/')
        
        # Should return 404 or 400, not 500
        assert response.status_code in [400, 404]
    
    def test_customer_without_account_returns_gracefully(self, db, customer_without_account):
        """
        Test API handles customer without account without error.
        
        Verifies:
        - 200 status (not an error)
        - Customer data present
        - Account and usage are None
        """
        client = Client()
        response = client.get(f'/api/customers/{customer_without_account.id}/usage/')
        
        assert response.status_code == 200
        data = response.json()
        assert data['customer'] is not None
        assert data['account'] is None
        assert data['usage'] is None
    
    def test_customer_without_usage_returns_gracefully(self, db, sample_customer, sample_account):
        """
        Test API handles customer with account but no usage.
        
        Verifies:
        - 200 status
        - Customer and account present
        - Usage is None
        """
        client = Client()
        response = client.get(f'/api/customers/{sample_customer.id}/usage/')
        
        assert response.status_code == 200
        data = response.json()
        assert data['customer'] is not None
        assert data['account'] is not None
        assert data['usage'] is None
    
    def test_invalid_email_format_validation(self, db):
        """
        Test customer creation validates email format.
        
        Verifies:
        - Invalid email formats are rejected
        - Validation error message returned
        """
        from django.core.exceptions import ValidationError
        
        customer = Customer(
            customer_code='EMAIL-001',
            first_name='Invalid',
            last_name='Email',
            email='not-an-email'  # Invalid format
        )
        
        with pytest.raises(ValidationError):
            customer.full_clean()
    
    def test_invalid_phone_number_format_validation(self, db):
        """
        Test customer creation validates phone number format.
        
        Verifies:
        - Invalid phone formats are rejected
        - Validation follows E.164 standard
        """
        from django.core.exceptions import ValidationError
        
        customer = Customer(
            customer_code='PHONE-001',
            first_name='Invalid',
            last_name='Phone',
            email='valid@test.com',
            phone_number='123'  # Too short
        )
        
        with pytest.raises(ValidationError):
            customer.full_clean()
    
    def test_negative_usage_values_rejected(self, db, sample_customer):
        """
        Test negative usage values are rejected.
        
        Verifies:
        - Negative data/minutes/SMS rejected
        - MinValueValidator works
        """
        from django.core.exceptions import ValidationError
        
        today = date.today()
        usage = UsageRecord(
            customer=sample_customer,
            billing_period_start=today,
            billing_period_end=today + timedelta(days=30),
            data_used_mb=Decimal('-100.00'),  # Invalid!
            data_limit_mb=Decimal('10240.00'),
            minutes_used=-10,  # Invalid!
            minutes_limit=500
        )
        
        with pytest.raises(ValidationError):
            usage.full_clean()
    
    def test_api_returns_json_for_all_errors(self, db):
        """
        Test API returns JSON for errors, not HTML.
        
        Verifies:
        - Content-Type is application/json
        - Error response is valid JSON
        """
        client = Client()
        response = client.get('/api/customers/999999/')
        
        assert response.status_code == 404
        assert 'application/json' in response['Content-Type']
        
        # Should be able to parse as JSON
        data = response.json()
        assert isinstance(data, dict)
    
    def test_empty_search_returns_all_customers(self, db, multiple_customers):
        """
        Test empty search query returns all customers.
        
        Verifies:
        - Empty search doesn't error
        - Returns all customers
        """
        client = Client()
        response = client.get('/api/customers/?search=')
        
        assert response.status_code == 200
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        
        assert len(results) >= 5
    
    def test_search_with_no_matches_returns_empty_list(self, db, multiple_customers):
        """
        Test search with no matches returns empty list, not error.
        
        Verifies:
        - No matches returns []
        - 200 status (not 404)
        """
        client = Client()
        response = client.get('/api/customers/?search=NonExistentCustomer12345')
        
        assert response.status_code == 200
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
            assert len(results) == 0
        else:
            assert len(data) == 0
            assert isinstance(data, list)
    
    def test_usage_with_zero_limit_percentage_handling(self, db, sample_customer):
        """
        Test percentage calculation doesn't divide by zero.
        
        Verifies:
        - Zero limit handled gracefully
        - Percentage returns None (like unlimited)
        """
        today = date.today()
        usage = UsageRecord.objects.create(
            customer=sample_customer,
            billing_period_start=today,
            billing_period_end=today + timedelta(days=30),
            data_used_mb=Decimal('1000.00'),
            data_limit_mb=Decimal('0.00'),  # Edge case
            minutes_used=100,
            minutes_limit=0  # Edge case
        )
        
        # Should not raise exception
        assert usage.data_used_percentage is None or usage.data_used_percentage >= 0
        assert usage.minutes_used_percentage is None or usage.minutes_used_percentage >= 0
    
    def test_concurrent_account_creation_conflict(self, db, sample_customer, sample_account):
        """
        Test concurrent account creation is prevented.
        
        Verifies:
        - One-to-one constraint enforced
        - Second account creation fails
        """
        from django.db import IntegrityError
        
        with pytest.raises(IntegrityError):
            Account.objects.create(
                customer=sample_customer,  # Already has account
                balance=Decimal('1000.00')
            )
    
    def test_malformed_date_in_billing_period(self, db, sample_customer):
        """
        Test billing period with invalid dates is rejected.
        
        Verifies:
        - End date before start date rejected
        - Database constraint enforced
        """
        from django.db import IntegrityError
        
        today = date.today()
        
        with pytest.raises(IntegrityError):
            UsageRecord.objects.create(
                customer=sample_customer,
                billing_period_start=today,
                billing_period_end=today - timedelta(days=1),  # Before start!
                data_used_mb=Decimal('1000.00')
            )
    
    def test_account_balance_below_minimum(self, db):
        """
        Test account balance below minimum is rejected.
        
        Verifies:
        - Balance constraint enforced
        - Cannot go below -1000.00
        """
        from django.db import IntegrityError
        
        customer = Customer.objects.create(
            customer_code='BAL-TEST-001',
            first_name='Balance',
            last_name='Test',
            email='balance@test.com'
        )
        
        with pytest.raises(IntegrityError):
            Account.objects.create(
                customer=customer,
                balance=Decimal('-1001.00')  # Below minimum
            )
    
    def test_duplicate_customer_code_rejected(self, db, sample_customer):
        """
        Test duplicate customer code is rejected.
        
        Verifies:
        - Unique constraint enforced
        - Proper error returned
        """
        from django.db import IntegrityError
        
        with pytest.raises(IntegrityError):
            Customer.objects.create(
                customer_code='TEST-001',  # Duplicate
                first_name='Another',
                last_name='User',
                email='another@test.com'
            )
    
    def test_duplicate_email_rejected(self, db, sample_customer):
        """
        Test duplicate email is rejected.
        
        Verifies:
        - Unique constraint enforced
        - Email uniqueness maintained
        """
        from django.db import IntegrityError
        
        with pytest.raises(IntegrityError):
            Customer.objects.create(
                customer_code='TEST-002',
                first_name='Another',
                last_name='User',
                email='john.doe@test.com'  # Duplicate
            )
    
    def test_health_check_always_returns_200(self, db):
        """
        Test health check endpoint is always accessible.
        
        Verifies:
        - Health endpoint doesn't fail
        - Returns proper status
        """
        client = Client()
        response = client.get('/api/health/')
        
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
    
    def test_api_handles_large_result_sets(self, db):
        """
        Test API can handle many customers without error.
        
        Verifies:
        - Large result sets don't cause timeout
        - Pagination or limits work if implemented
        """
        # Create 100 customers
        for i in range(100):
            Customer.objects.create(
                customer_code=f'LOAD-{i:04d}',
                first_name=f'User{i}',
                last_name=f'Test{i}',
                email=f'user{i}@loadtest.com'
            )
        
        client = Client()
        response = client.get('/api/customers/')
        
        assert response.status_code == 200
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'count' in data:
            # Paginated - check total count
            assert data['count'] >= 100
        else:
            # Non-paginated - check results length
            assert len(data) >= 100
    
    def test_decimal_precision_maintained(self, db, sample_customer):
        """
        Test decimal values maintain precision.
        
        Verifies:
        - Decimal fields don't lose precision
        - Calculations are accurate
        """
        today = date.today()
        usage = UsageRecord.objects.create(
            customer=sample_customer,
            billing_period_start=today,
            billing_period_end=today + timedelta(days=30),
            data_used_mb=Decimal('1234.56'),  # Precise value
            data_limit_mb=Decimal('10240.00'),
            minutes_used=123,
            minutes_limit=500
        )
        
        # Refresh from DB
        usage.refresh_from_db()
        
        # Precision should be maintained
        assert usage.data_used_mb == Decimal('1234.56')
        
        # Percentage calculation should be accurate
        expected_percentage = round((1234.56 / 10240.00) * 100, 2)
        assert usage.data_used_percentage == expected_percentage
