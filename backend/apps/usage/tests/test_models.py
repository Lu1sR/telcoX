"""
Unit tests for UsageRecord model
"""
from django.test import TestCase
from decimal import Decimal
from datetime import date, timedelta
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord


class UsageRecordModelTestCase(TestCase):
    """Test cases for UsageRecord model"""

    def setUp(self):
        """Set up test data"""
        self.customer = Customer.objects.create(
            customer_code='CUST-001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )
        self.account = Account.objects.create(
            customer=self.customer,
            balance=Decimal('1000.00')
        )
        
        self.usage_data = {
            'customer': self.customer,
            'billing_period_start': date(2025, 1, 1),
            'billing_period_end': date(2025, 1, 31),
            'data_used_mb': Decimal('1500.00'),
            'data_limit_mb': Decimal('2000.00'),
            'minutes_used': 250,
            'minutes_limit': 500,
            'sms_used': 50,
            'sms_limit': 100
        }

    def test_create_usage_record_with_valid_data(self):
        """Test creating a usage record with valid data"""
        usage = UsageRecord.objects.create(**self.usage_data)
        
        self.assertEqual(usage.customer, self.customer)
        self.assertEqual(usage.data_used_mb, Decimal('1500.00'))
        self.assertEqual(usage.data_limit_mb, Decimal('2000.00'))
        self.assertEqual(usage.minutes_used, 250)
        self.assertEqual(usage.minutes_limit, 500)
        self.assertEqual(usage.sms_used, 50)
        self.assertEqual(usage.sms_limit, 100)

    def test_usage_record_default_values(self):
        """Test usage record default values"""
        usage = UsageRecord.objects.create(
            customer=self.customer,
            billing_period_start=date(2025, 1, 1),
            billing_period_end=date(2025, 1, 31)
        )
        
        self.assertEqual(usage.data_used_mb, Decimal('0.00'))
        self.assertIsNone(usage.data_limit_mb)
        self.assertEqual(usage.minutes_used, 0)
        self.assertIsNone(usage.minutes_limit)
        self.assertEqual(usage.sms_used, 0)
        self.assertIsNone(usage.sms_limit)

    def test_usage_record_str_representation(self):
        """Test usage record string representation"""
        usage = UsageRecord.objects.create(**self.usage_data)
        expected = f"Usage for {self.account} (2025-01-01 to 2025-01-31)"
        self.assertEqual(str(usage), expected)

    def test_data_used_percentage_calculation(self):
        """Test data_used_percentage property calculation"""
        usage = UsageRecord.objects.create(**self.usage_data)
        
        # 1500 / 2000 = 75%
        self.assertEqual(usage.data_used_percentage, 75.0)

    def test_data_used_percentage_with_null_limit(self):
        """Test data_used_percentage when limit is null (unlimited)"""
        data = self.usage_data.copy()
        data['data_limit_mb'] = None
        usage = UsageRecord.objects.create(**data)
        
        self.assertIsNone(usage.data_used_percentage)

    def test_data_used_percentage_with_zero_limit(self):
        """Test data_used_percentage when limit is zero"""
        data = self.usage_data.copy()
        data['data_limit_mb'] = Decimal('0.00')
        usage = UsageRecord.objects.create(**data)
        
        self.assertIsNone(usage.data_used_percentage)

    def test_minutes_used_percentage_calculation(self):
        """Test minutes_used_percentage property calculation"""
        usage = UsageRecord.objects.create(**self.usage_data)
        
        # 250 / 500 = 50%
        self.assertEqual(usage.minutes_used_percentage, 50.0)

    def test_minutes_used_percentage_with_null_limit(self):
        """Test minutes_used_percentage when limit is null"""
        data = self.usage_data.copy()
        data['minutes_limit'] = None
        usage = UsageRecord.objects.create(**data)
        
        self.assertIsNone(usage.minutes_used_percentage)

    def test_sms_used_percentage_calculation(self):
        """Test sms_used_percentage property calculation"""
        usage = UsageRecord.objects.create(**self.usage_data)
        
        # 50 / 100 = 50%
        self.assertEqual(usage.sms_used_percentage, 50.0)

    def test_sms_used_percentage_with_null_limit(self):
        """Test sms_used_percentage when limit is null"""
        data = self.usage_data.copy()
        data['sms_limit'] = None
        usage = UsageRecord.objects.create(**data)
        
        self.assertIsNone(usage.sms_used_percentage)

    def test_over_limit_usage(self):
        """Test percentage calculation when usage exceeds limit"""
        data = self.usage_data.copy()
        data['data_used_mb'] = Decimal('2500.00')  # Exceeds 2000 limit
        usage = UsageRecord.objects.create(**data)
        
        # 2500 / 2000 = 125%
        self.assertEqual(usage.data_used_percentage, 125.0)

    def test_customer_can_have_multiple_usage_records(self):
        """Test that a customer can have multiple usage records"""
        usage1 = UsageRecord.objects.create(
            customer=self.customer,
            billing_period_start=date(2025, 1, 1),
            billing_period_end=date(2025, 1, 31),
            data_used_mb=Decimal('1000.00')
        )
        usage2 = UsageRecord.objects.create(
            customer=self.customer,
            billing_period_start=date(2025, 2, 1),
            billing_period_end=date(2025, 2, 28),
            data_used_mb=Decimal('800.00')
        )
        
        self.assertEqual(self.customer.usage_records.count(), 2)
        self.assertIn(usage1, self.customer.usage_records.all())
        self.assertIn(usage2, self.customer.usage_records.all())

    def test_usage_record_cascade_delete(self):
        """Test that deleting a customer deletes associated usage records"""
        UsageRecord.objects.create(**self.usage_data)
        UsageRecord.objects.create(
            customer=self.customer,
            billing_period_start=date(2025, 2, 1),
            billing_period_end=date(2025, 2, 28)
        )
        
        customer_id = self.customer.id
        self.assertEqual(UsageRecord.objects.filter(customer_id=customer_id).count(), 2)
        
        self.customer.delete()
        
        self.assertEqual(UsageRecord.objects.filter(customer_id=customer_id).count(), 0)
