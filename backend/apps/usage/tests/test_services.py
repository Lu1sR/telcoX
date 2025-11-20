"""
Unit tests for Usage service layer
"""
from django.test import TestCase
from decimal import Decimal
from datetime import date
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord
from apps.usage.services import UsageService


class UsageServiceTestCase(TestCase):
    """Test cases for UsageService"""

    def setUp(self):
        """Set up test data"""
        # Create customer with account and usage
        self.customer = Customer.objects.create(
            customer_code='CUST-001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='+1234567890'
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

    def test_get_customer_usage_overview_success(self):
        """Test getting customer usage overview with complete data"""
        result = UsageService.get_customer_usage_overview(self.customer.id)
        
        # Check customer data
        self.assertEqual(result['customer']['id'], self.customer.id)
        self.assertEqual(result['customer']['customer_code'], 'CUST-001')
        self.assertEqual(result['customer']['first_name'], 'John')
        self.assertEqual(result['customer']['last_name'], 'Doe')
        self.assertEqual(result['customer']['email'], 'john.doe@example.com')
        
        # Check account data
        self.assertIsNotNone(result['account'])
        self.assertEqual(result['account']['id'], self.account.id)
        self.assertEqual(Decimal(result['account']['balance']), Decimal('1250.00'))
        self.assertEqual(result['account']['currency'], 'USD')
        self.assertEqual(result['account']['status'], 'ACTIVE')
        
        # Check usage data
        self.assertIsNotNone(result['usage'])
        self.assertEqual(result['usage']['id'], self.usage.id)
        self.assertEqual(Decimal(result['usage']['data_used_mb']), Decimal('1500.00'))
        self.assertEqual(Decimal(result['usage']['data_limit_mb']), Decimal('2000.00'))
        self.assertEqual(result['usage']['minutes_used'], 250)
        self.assertEqual(result['usage']['minutes_limit'], 500)
        self.assertEqual(result['usage']['sms_used'], 50)
        self.assertEqual(result['usage']['sms_limit'], 100)

    def test_get_customer_usage_overview_customer_not_found(self):
        """Test getting usage overview for non-existent customer"""
        result = UsageService.get_customer_usage_overview(999)
        self.assertIsNone(result)

    def test_get_customer_usage_overview_no_account(self):
        """Test getting usage overview when customer has no account"""
        # Create customer without account
        customer2 = Customer.objects.create(
            customer_code='CUST-002',
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )
        
        result = UsageService.get_customer_usage_overview(customer2.id)
        
        # Should return customer data but null account and usage
        self.assertIsNotNone(result)
        self.assertEqual(result['customer']['id'], customer2.id)
        self.assertIsNone(result['account'])
        self.assertIsNone(result['usage'])

    def test_get_customer_usage_overview_no_usage(self):
        """Test getting usage overview when account has no usage records"""
        # Create customer with account but no usage
        customer2 = Customer.objects.create(
            customer_code='CUST-002',
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )
        account2 = Account.objects.create(
            customer=customer2,
            balance=Decimal('500.00')
        )
        
        result = UsageService.get_customer_usage_overview(customer2.id)
        
        # Should return customer and account but null usage
        self.assertIsNotNone(result)
        self.assertEqual(result['customer']['id'], customer2.id)
        self.assertIsNotNone(result['account'])
        self.assertEqual(result['account']['id'], account2.id)
        self.assertIsNone(result['usage'])

    def test_get_customer_usage_overview_with_account(self):
        """Test getting usage overview when customer has an account"""
        result = UsageService.get_customer_usage_overview(self.customer.id)
        
        # Should return the customer's account
        self.assertIsNotNone(result['account'])
        self.assertEqual(result['account']['id'], self.account.id)
        self.assertEqual(Decimal(result['account']['balance']), Decimal('1250.00'))

    def test_get_customer_usage_overview_multiple_usage_records(self):
        """Test getting usage overview when account has multiple usage records"""
        # Create second usage record
        usage2 = UsageRecord.objects.create(
            customer=self.customer,
            billing_period_start=date(2024, 12, 1),
            billing_period_end=date(2024, 12, 31),
            data_used_mb=Decimal('800.00')
        )
        
        result = UsageService.get_customer_usage_overview(self.customer.id)
        
        # Should return the most recent usage record
        self.assertIsNotNone(result['usage'])
        self.assertEqual(result['usage']['id'], self.usage.id)

    def test_get_customer_usage_overview_percentage_calculations(self):
        """Test that percentage calculations are included"""
        result = UsageService.get_customer_usage_overview(self.customer.id)
        
        # Check percentage fields exist and are correct
        self.assertEqual(result['usage']['data_used_percentage'], 75.0)
        self.assertEqual(result['usage']['minutes_used_percentage'], 50.0)
        self.assertEqual(result['usage']['sms_used_percentage'], 50.0)

    def test_get_customer_usage_overview_unlimited_plan(self):
        """Test usage overview with unlimited plan (null limits)"""
        # Create usage with null limits
        self.usage.data_limit_mb = None
        self.usage.minutes_limit = None
        self.usage.sms_limit = None
        self.usage.save()
        
        result = UsageService.get_customer_usage_overview(self.customer.id)
        
        # Percentages should be None for unlimited
        self.assertIsNone(result['usage']['data_used_percentage'])
        self.assertIsNone(result['usage']['minutes_used_percentage'])
        self.assertIsNone(result['usage']['sms_used_percentage'])
