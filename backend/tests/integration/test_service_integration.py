"""
Service Layer Integration Tests.

These tests verify service methods work correctly with real database operations.
Tests cover business logic, data aggregation, and edge cases.
"""
import pytest
from decimal import Decimal
from apps.usage.services import UsageService
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord


@pytest.mark.integration
class TestUsageServiceIntegration:
    """Test service layer with real database."""
    
    def test_get_customer_usage_overview_with_real_db(self, db, customer_with_full_data):
        """
        Test UsageService.get_customer_usage_overview() with real database.
        
        Verifies:
        - Service correctly queries database
        - Returns proper data structure
        - Percentage calculations are accurate
        - All serializers work correctly
        """
        customer, account, usage_record = customer_with_full_data
        
        service = UsageService()
        result = service.get_customer_usage_overview(customer.id)
        
        # Verify result structure
        assert result is not None
        assert 'customer' in result
        assert 'account' in result
        assert 'usage' in result
        
        # Verify customer data
        assert result['customer']['id'] == customer.id
        assert result['customer']['customer_code'] == 'FULL-001'
        assert result['customer']['first_name'] == 'Jane'
        assert result['customer']['last_name'] == 'Smith'
        
        # Verify account data
        assert result['account']['id'] == account.id
        assert Decimal(result['account']['balance']) == Decimal('2500.00')
        
        # Verify usage data
        assert Decimal(result['usage']['data_used_mb']) == Decimal('7680.00')
        assert result['usage']['minutes_used'] == 375
        
        # Verify percentages
        assert result['usage']['data_used_percentage'] == 75.0
        assert result['usage']['minutes_used_percentage'] == 75.0
        assert result['usage']['sms_used_percentage'] == 75.0
    
    def test_usage_service_returns_none_for_nonexistent_customer(self, db):
        """
        Test service returns None for non-existent customer.
        
        Verifies:
        - Service handles missing customer gracefully
        - No exception is raised
        - Returns None as expected
        """
        service = UsageService()
        result = service.get_customer_usage_overview(999999)
        
        assert result is None
    
    def test_usage_service_handles_customer_without_account(self, db, customer_without_account):
        """
        Test service handles customers without accounts.
        
        Verifies:
        - Returns customer data
        - Account field is None
        - Usage field is None
        - No exception raised
        """
        service = UsageService()
        result = service.get_customer_usage_overview(customer_without_account.id)
        
        assert result is not None
        assert result['customer']['id'] == customer_without_account.id
        assert result['account'] is None
        assert result['usage'] is None
    
    def test_usage_service_handles_customer_without_usage(self, db, sample_customer, sample_account):
        """
        Test service handles customer with account but no usage records.
        
        Verifies:
        - Returns customer and account data
        - Usage field is None
        - No exception raised
        """
        service = UsageService()
        result = service.get_customer_usage_overview(sample_customer.id)
        
        assert result is not None
        assert result['customer']['id'] == sample_customer.id
        assert result['account']['id'] == sample_account.id
        assert result['usage'] is None
    
    def test_usage_service_returns_most_recent_usage(self, db, sample_customer, sample_account):
        """
        Test service returns the most recent usage record.
        
        Verifies:
        - Multiple usage records handled correctly
        - Most recent record by billing_period_end is returned
        - Ordering works as expected
        """
        from datetime import date, timedelta
        
        # Create multiple usage records
        today = date.today()
        
        # Older record
        older_usage = UsageRecord.objects.create(
            customer=sample_customer,
            billing_period_start=today - timedelta(days=60),
            billing_period_end=today - timedelta(days=30),
            data_used_mb=Decimal('1000.00'),
            data_limit_mb=Decimal('10240.00'),
            minutes_used=100,
            minutes_limit=500
        )
        
        # Newer record
        newer_usage = UsageRecord.objects.create(
            customer=sample_customer,
            billing_period_start=today - timedelta(days=30),
            billing_period_end=today,
            data_used_mb=Decimal('5000.00'),
            data_limit_mb=Decimal('10240.00'),
            minutes_used=250,
            minutes_limit=500
        )
        
        service = UsageService()
        result = service.get_customer_usage_overview(sample_customer.id)
        
        # Should return newer record
        assert result['usage']['id'] == newer_usage.id
        assert Decimal(result['usage']['data_used_mb']) == Decimal('5000.00')
        assert result['usage']['minutes_used'] == 250
    
    def test_usage_service_with_unlimited_plan(self, db, customer_with_unlimited_plan):
        """
        Test service handles unlimited plans correctly.
        
        Verifies:
        - Null limits are handled properly
        - Percentage calculations return None
        - No division by zero errors
        """
        customer, account, usage_record = customer_with_unlimited_plan
        
        service = UsageService()
        result = service.get_customer_usage_overview(customer.id)
        
        assert result is not None
        assert result['usage']['data_limit_mb'] is None
        assert result['usage']['minutes_limit'] is None
        assert result['usage']['sms_limit'] is None
        
        # Percentages should be None for unlimited
        assert result['usage']['data_used_percentage'] is None
        assert result['usage']['minutes_used_percentage'] is None
        assert result['usage']['sms_used_percentage'] is None
    
    def test_usage_service_with_high_usage(self, db, customer_with_high_usage):
        """
        Test service correctly calculates high usage percentages.
        
        Verifies:
        - Percentages over 90% calculated correctly
        - No rounding errors
        - Decimal precision maintained
        """
        customer, account, usage_record = customer_with_high_usage
        
        service = UsageService()
        result = service.get_customer_usage_overview(customer.id)
        
        # Verify high percentages
        assert result['usage']['data_used_percentage'] > 90.0
        assert result['usage']['minutes_used_percentage'] > 90.0
        assert result['usage']['sms_used_percentage'] > 90.0
        
        # Verify specific values
        assert result['usage']['data_used_percentage'] == 92.77
        assert result['usage']['minutes_used_percentage'] == 96.0
        assert result['usage']['sms_used_percentage'] == 95.0
    
    def test_usage_service_serializer_includes_all_fields(self, db, customer_with_full_data):
        """
        Test service returns all expected fields.
        
        Verifies:
        - Customer serializer includes all fields
        - Account serializer includes all fields
        - Usage serializer includes all fields
        """
        customer, account, usage_record = customer_with_full_data
        
        service = UsageService()
        result = service.get_customer_usage_overview(customer.id)
        
        # Check customer fields
        customer_fields = ['id', 'customer_code', 'first_name', 'last_name', 'email']
        for field in customer_fields:
            assert field in result['customer'], f"Missing customer field: {field}"
        
        # Check account fields
        account_fields = ['id', 'balance', 'currency', 'status']
        for field in account_fields:
            assert field in result['account'], f"Missing account field: {field}"
        
        # Check usage fields
        usage_fields = [
            'id', 'data_used_mb', 'data_limit_mb', 
            'minutes_used', 'minutes_limit',
            'sms_used', 'sms_limit',
            'data_used_percentage', 'minutes_used_percentage', 'sms_used_percentage'
        ]
        for field in usage_fields:
            assert field in result['usage'], f"Missing usage field: {field}"
    
    def test_usage_service_handles_zero_usage(self, db, sample_customer, sample_account):
        """
        Test service handles zero usage correctly.
        
        Verifies:
        - Zero usage percentages calculated as 0.0
        - No errors with zero values
        """
        from datetime import date, timedelta
        
        today = date.today()
        usage = UsageRecord.objects.create(
            customer=sample_customer,
            billing_period_start=today,
            billing_period_end=today + timedelta(days=30),
            data_used_mb=Decimal('0.00'),
            data_limit_mb=Decimal('10240.00'),
            minutes_used=0,
            minutes_limit=500,
            sms_used=0,
            sms_limit=100
        )
        
        service = UsageService()
        result = service.get_customer_usage_overview(sample_customer.id)
        
        assert result['usage']['data_used_percentage'] == 0.0
        assert result['usage']['minutes_used_percentage'] == 0.0
        assert result['usage']['sms_used_percentage'] == 0.0
    
    def test_usage_service_handles_exceeded_limits(self, db, sample_customer, sample_account):
        """
        Test service handles usage exceeding limits.
        
        Verifies:
        - Percentages over 100% calculated correctly
        - System doesn't cap at 100%
        """
        from datetime import date, timedelta
        
        today = date.today()
        usage = UsageRecord.objects.create(
            customer=sample_customer,
            billing_period_start=today,
            billing_period_end=today + timedelta(days=30),
            data_used_mb=Decimal('15000.00'),  # Exceeds 10240 limit
            data_limit_mb=Decimal('10240.00'),
            minutes_used=600,  # Exceeds 500 limit
            minutes_limit=500,
            sms_used=150,  # Exceeds 100 limit
            sms_limit=100
        )
        
        service = UsageService()
        result = service.get_customer_usage_overview(sample_customer.id)
        
        # Verify percentages can exceed 100%
        assert result['usage']['data_used_percentage'] > 100.0
        assert result['usage']['minutes_used_percentage'] > 100.0
        assert result['usage']['sms_used_percentage'] > 100.0
        
        # Verify specific calculations
        assert result['usage']['data_used_percentage'] == 146.48
        assert result['usage']['minutes_used_percentage'] == 120.0
        assert result['usage']['sms_used_percentage'] == 150.0
    
    def test_usage_service_database_query_efficiency(self, db, customer_with_full_data):
        """
        Test service makes efficient database queries.
        
        Verifies:
        - Service uses select_related/prefetch_related appropriately
        - Number of queries is minimal
        """
        from django.test.utils import override_settings
        from django.db import connection
        from django.test import TestCase
        
        customer, account, usage_record = customer_with_full_data
        
        # Reset query count
        connection.queries_log.clear()
        
        service = UsageService()
        result = service.get_customer_usage_overview(customer.id)
        
        # Service should make reasonable number of queries
        # Exact number depends on implementation, but should be low
        query_count = len(connection.queries)
        assert query_count <= 10, f"Too many queries: {query_count}"
