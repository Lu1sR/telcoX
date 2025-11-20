"""
Unit tests for Usage API views
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord


class UsageAPITestCase(TestCase):
    """Test cases for Usage API endpoints"""

    def setUp(self):
        """Set up test client and data"""
        self.client = APIClient()
        
        # Create test customer with account and usage
        self.customer = Customer.objects.create(
            customer_code='CUST-001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )
        self.account = Account.objects.create(
            customer=self.customer,
            balance=Decimal('1250.00'),
            currency='USD',
            status='ACTIVE'
        )
        self.usage = UsageRecord.objects.create(
            customer=self.customer,
            billing_period_start=date(2025, 1, 1),
            billing_period_end=date(2025, 1, 31),
            data_used_mb=Decimal('1500.00'),
            data_limit_mb=Decimal('2000.00'),
            minutes_used=250,
            minutes_limit=500,
            sms_used=50,
            sms_limit=100
        )

    def test_get_customer_usage_overview(self):
        """Test GET /api/customers/{id}/usage/ returns combined data"""
        response = self.client.get(f'/api/customers/{self.customer.id}/usage/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify customer data
        self.assertEqual(response.data['customer']['customer_code'], 'CUST-001')
        self.assertEqual(response.data['customer']['first_name'], 'John')
        
        # Verify account data
        self.assertIsNotNone(response.data['account'])
        self.assertEqual(response.data['account']['currency'], 'USD')
        
        # Verify usage data
        self.assertIsNotNone(response.data['usage'])
        self.assertEqual(response.data['usage']['data_used_percentage'], 75.0)

    def test_get_customer_usage_overview_not_found(self):
        """Test GET /api/customers/{id}/usage/ with invalid ID returns 404"""
        response = self.client.get('/api/customers/999/usage/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_usage_records_list(self):
        """Test GET /api/usage/ returns list of usage records"""
        response = self.client.get('/api/usage/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_usage_endpoint_is_read_only(self):
        """Test that POST/PUT/DELETE are not allowed on usage endpoint"""
        # Try POST
        response = self.client.post('/api/usage/', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
