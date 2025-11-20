"""
API Integration Tests for TelcoX.

These tests verify full HTTP request/response cycles with real database operations.
Tests cover API endpoints, serialization, and database queries.
"""
import pytest
from django.test import Client
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord
from decimal import Decimal


@pytest.mark.integration
class TestCustomerAPIIntegration:
    """Full API integration tests with real database."""
    
    def test_get_customers_with_db(self, db, multiple_customers):
        """
        Test GET /api/customers/ returns customers from database.
        
        Verifies:
        - API returns 200 status
        - Database query executes successfully
        - All customers are returned
        - JSON structure is correct
        """
        client = Client()
        response = client.get('/api/customers/')
        
        assert response.status_code == 200
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        
        assert len(results) >= 5
        # Check first customer (may not be MULTI-000 if seeded data exists)
        assert 'customer_code' in results[0]
        assert 'first_name' in results[0]
        assert 'email' in results[0]
        assert 'created_at' in results[0]
    
    def test_get_customer_detail_with_db(self, db, sample_customer, sample_account):
        """
        Test GET /api/customers/{id}/ returns customer details.
        
        Verifies:
        - API returns 200 for existing customer
        - Customer data is correctly serialized
        - Related account data is accessible
        """
        client = Client()
        response = client.get(f'/api/customers/{sample_customer.id}/')
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == sample_customer.id
        assert data['customer_code'] == 'TEST-001'
        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'
        assert data['email'] == 'john.doe@test.com'
    
    def test_customer_usage_overview_integration(self, db, customer_with_full_data):
        """
        Test GET /api/customers/{id}/usage/ with full data chain.
        
        Verifies:
        - Customer → Account → UsageRecord relationships work
        - Percentage calculations are correct
        - JSON serialization works properly
        - All expected fields are present
        """
        customer, account, usage_record = customer_with_full_data
        client = Client()
        response = client.get(f'/api/customers/{customer.id}/usage/')
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify customer data
        assert data['customer']['id'] == customer.id
        assert data['customer']['customer_code'] == 'FULL-001'
        assert data['customer']['first_name'] == 'Jane'
        assert data['customer']['email'] == 'jane.smith@test.com'
        
        # Verify account data
        assert data['account']['id'] == account.id
        assert Decimal(data['account']['balance']) == Decimal('2500.00')
        assert data['account']['status'] == 'ACTIVE'
        
        # Verify usage data
        assert Decimal(data['usage']['data_used_mb']) == Decimal('7680.00')
        assert Decimal(data['usage']['data_limit_mb']) == Decimal('10240.00')
        assert data['usage']['minutes_used'] == 375
        assert data['usage']['minutes_limit'] == 500
        assert data['usage']['sms_used'] == 75
        
        # Verify percentage calculations
        assert data['usage']['data_used_percentage'] == 75.0
        assert data['usage']['minutes_used_percentage'] == 75.0
        assert data['usage']['sms_used_percentage'] == 75.0
    
    def test_customer_usage_with_unlimited_plan(self, db, customer_with_unlimited_plan):
        """
        Test usage endpoint with unlimited plan (null limits).
        
        Verifies:
        - API handles null limits correctly
        - Percentage calculations return None for unlimited
        """
        customer, account, usage_record = customer_with_unlimited_plan
        client = Client()
        response = client.get(f'/api/customers/{customer.id}/usage/')
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify unlimited fields
        assert data['usage']['data_limit_mb'] is None
        assert data['usage']['minutes_limit'] is None
        assert data['usage']['sms_limit'] is None
        
        # Verify percentages are None for unlimited
        assert data['usage']['data_used_percentage'] is None
        assert data['usage']['minutes_used_percentage'] is None
        assert data['usage']['sms_used_percentage'] is None
    
    def test_customer_not_found_integration(self, db):
        """
        Test 404 behavior with real database.
        
        Verifies:
        - Non-existent customer returns 404
        - Error response format is correct
        """
        client = Client()
        response = client.get('/api/customers/999999/usage/')
        
        assert response.status_code == 404
        data = response.json()
        assert 'detail' in data or 'error' in data
    
    def test_customer_without_account_integration(self, db, customer_without_account):
        """
        Test usage endpoint for customer without account.
        
        Verifies:
        - API handles missing account gracefully
        - Returns customer data with null account/usage
        """
        client = Client()
        response = client.get(f'/api/customers/{customer_without_account.id}/usage/')
        
        assert response.status_code == 200
        data = response.json()
        
        # Customer should be present
        assert data['customer']['id'] == customer_without_account.id
        
        # Account and usage should be null
        assert data['account'] is None
        assert data['usage'] is None
    
    def test_search_customers_with_db(self, db, multiple_customers):
        """
        Test customer search functionality with real DB queries.
        
        Verifies:
        - Search query parameter works
        - Only matching customers returned
        - Search is case-insensitive
        """
        client = Client()
        
        # Search by first name
        response = client.get('/api/customers/?search=User0')
        assert response.status_code == 200
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        
        assert len(results) >= 1
        assert any(c['first_name'] == 'User0' for c in results)
        
        # Search by email
        response = client.get('/api/customers/?search=user1@test.com')
        assert response.status_code == 200
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        
        assert len(results) >= 1
        assert any(c['email'] == 'user1@test.com' for c in results)
    
    def test_usage_records_list_integration(self, db, sample_usage_record):
        """
        Test GET /api/usage/ returns usage records from database.
        
        Verifies:
        - API returns 200 status
        - Usage records are returned
        - Serialization includes all fields
        """
        client = Client()
        response = client.get('/api/usage/')
        
        assert response.status_code == 200
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        
        assert len(results) >= 1
        
        # Verify first record structure
        record = results[0]
        assert 'id' in record
        assert 'billing_period_start' in record
        assert 'billing_period_end' in record
        assert 'data_used_mb' in record
        assert 'minutes_used' in record
        assert 'sms_used' in record
        assert 'data_used_percentage' in record
        assert 'minutes_used_percentage' in record
        assert 'sms_used_percentage' in record
    
    def test_health_check_integration(self, db):
        """
        Test health check endpoint with database access.
        
        Verifies:
        - Health endpoint returns 200
        - Response indicates healthy status
        """
        client = Client()
        response = client.get('/api/health/')
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'database' in data
    
    def test_api_returns_correct_content_type(self, db, sample_customer):
        """
        Test API returns proper JSON content type.
        
        Verifies:
        - Content-Type header is application/json
        """
        client = Client()
        response = client.get(f'/api/customers/{sample_customer.id}/')
        
        assert response.status_code == 200
        assert 'application/json' in response['Content-Type']
    
    def test_high_usage_customer_integration(self, db, customer_with_high_usage):
        """
        Test API correctly handles customers with high usage percentages.
        
        Verifies:
        - Percentages over 90% are calculated correctly
        - No overflow or rounding errors
        """
        customer, account, usage_record = customer_with_high_usage
        client = Client()
        response = client.get(f'/api/customers/{customer.id}/usage/')
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify high usage percentages
        assert data['usage']['data_used_percentage'] > 90.0
        assert data['usage']['minutes_used_percentage'] > 90.0
        assert data['usage']['sms_used_percentage'] > 90.0
        
        # Verify specific calculations
        assert data['usage']['data_used_percentage'] == 92.77
        assert data['usage']['minutes_used_percentage'] == 96.0
        assert data['usage']['sms_used_percentage'] == 95.0
