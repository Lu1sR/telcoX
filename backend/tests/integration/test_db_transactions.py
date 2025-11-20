"""
Database Transaction Integration Tests.

These tests verify database-level operations including:
- Cascade deletions
- Data integrity
- Foreign key relationships
- Constraints
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from django.db import transaction, IntegrityError
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord


@pytest.mark.integration
class TestDatabaseTransactions:
    """Test database-level operations and transactions."""
    
    def test_cascade_delete_customer(self, db, customer_with_full_data):
        """
        Test that deleting customer cascades to account and usage records.
        
        Verifies:
        - Customer deletion triggers cascade
        - Related account is deleted
        - Related usage records are deleted
        - Database foreign key constraints work correctly
        """
        customer, account, usage_record = customer_with_full_data
        
        # Store IDs before deletion
        customer_id = customer.id
        account_id = account.id
        usage_id = usage_record.id
        
        # Delete customer
        customer.delete()
        
        # Verify cascade deletion
        assert not Customer.objects.filter(id=customer_id).exists()
        assert not Account.objects.filter(id=account_id).exists()
        assert not UsageRecord.objects.filter(id=usage_id).exists()
    
    def test_cascade_delete_account(self, db, sample_customer, sample_account):
        """
        Test that deleting account does not delete customer.
        
        Verifies:
        - Account can be deleted independently
        - Customer remains after account deletion
        - Foreign key relationship is one-to-one
        """
        customer_id = sample_customer.id
        account_id = sample_account.id
        
        # Delete account
        sample_account.delete()
        
        # Verify account deleted but customer remains
        assert Customer.objects.filter(id=customer_id).exists()
        assert not Account.objects.filter(id=account_id).exists()
    
    def test_usage_records_cascade_with_customer(self, db, sample_customer):
        """
        Test multiple usage records are deleted when customer is deleted.
        
        Verifies:
        - Multiple related records cascade properly
        - Database handles batch deletions
        """
        # Create multiple usage records for the same customer
        today = date.today()
        usage_records = []
        
        for i in range(3):
            start_date = today.replace(day=1) - timedelta(days=30 * i)
            end_date = start_date + timedelta(days=30)
            usage = UsageRecord.objects.create(
                customer=sample_customer,
                billing_period_start=start_date,
                billing_period_end=end_date,
                data_used_mb=Decimal('1000.00'),
                data_limit_mb=Decimal('10240.00'),
                minutes_used=100,
                minutes_limit=500,
                sms_used=50,
                sms_limit=100
            )
            usage_records.append(usage.id)
        
        # Verify all records exist
        assert UsageRecord.objects.filter(customer=sample_customer).count() == 3
        
        # Delete customer
        customer_id = sample_customer.id
        sample_customer.delete()
        
        # Verify all usage records deleted
        assert not Customer.objects.filter(id=customer_id).exists()
        for usage_id in usage_records:
            assert not UsageRecord.objects.filter(id=usage_id).exists()
    
    def test_unique_customer_code_constraint(self, db, sample_customer):
        """
        Test unique constraint on customer_code.
        
        Verifies:
        - Duplicate customer codes are rejected
        - Database constraint is enforced
        """
        with pytest.raises(IntegrityError):
            Customer.objects.create(
                customer_code='TEST-001',  # Duplicate!
                first_name='Another',
                last_name='User',
                email='another@test.com'
            )
    
    def test_unique_email_constraint(self, db, sample_customer):
        """
        Test unique constraint on email.
        
        Verifies:
        - Duplicate emails are rejected
        - Database constraint is enforced
        """
        with pytest.raises(IntegrityError):
            Customer.objects.create(
                customer_code='TEST-002',
                first_name='Another',
                last_name='User',
                email='john.doe@test.com'  # Duplicate!
            )
    
    def test_one_to_one_account_constraint(self, db, sample_customer, sample_account):
        """
        Test one-to-one relationship between customer and account.
        
        Verifies:
        - Only one account per customer is allowed
        - Attempting to create second account fails
        """
        with pytest.raises(IntegrityError):
            Account.objects.create(
                customer=sample_customer,  # Already has account!
                balance=Decimal('1000.00')
            )
    
    def test_balance_minimum_constraint(self, db, sample_customer):
        """
        Test account balance minimum constraint.
        
        Verifies:
        - Balance cannot go below -1000.00
        - Database constraint is enforced
        """
        # This should work (within limit)
        account = Account.objects.create(
            customer=sample_customer,
            balance=Decimal('-999.00')
        )
        assert account.balance == Decimal('-999.00')
        
        # This should fail (below limit)
        with pytest.raises(IntegrityError):
            Account.objects.create(
                customer=Customer.objects.create(
                    customer_code='BAL-001',
                    first_name='Balance',
                    last_name='Test',
                    email='balance@test.com'
                ),
                balance=Decimal('-1001.00')  # Below minimum!
            )
    
    def test_billing_period_dates_constraint(self, db, sample_customer):
        """
        Test billing period date validation constraint.
        
        Verifies:
        - End date must be >= start date
        - Invalid date ranges are rejected
        """
        today = date.today()
        
        with pytest.raises(IntegrityError):
            UsageRecord.objects.create(
                customer=sample_customer,
                billing_period_start=today,
                billing_period_end=today - timedelta(days=1),  # End before start!
                data_used_mb=Decimal('1000.00')
            )
    
    def test_data_consistency_after_multiple_writes(self, db, sample_customer):
        """
        Test data remains consistent after series of writes.
        
        Verifies:
        - Multiple sequential operations succeed
        - Foreign key relationships remain intact
        - Data integrity is maintained
        """
        # Create account
        account = Account.objects.create(
            customer=sample_customer,
            balance=Decimal('1000.00')
        )
        
        # Create multiple usage records
        today = date.today()
        for i in range(5):
            start = today - timedelta(days=30 * (i + 1))
            end = today - timedelta(days=30 * i)
            UsageRecord.objects.create(
                customer=sample_customer,
                billing_period_start=start,
                billing_period_end=end,
                data_used_mb=Decimal('1000.00') * (i + 1),
                data_limit_mb=Decimal('10240.00'),
                minutes_used=100 * (i + 1),
                minutes_limit=500,
                sms_used=50 * (i + 1),
                sms_limit=100
            )
        
        # Verify all relationships intact
        assert sample_customer.account.id == account.id
        assert sample_customer.usage_records.count() == 5
        assert all(
            ur.customer_id == sample_customer.id 
            for ur in sample_customer.usage_records.all()
        )
    
    def test_transaction_rollback_on_error(self, db, sample_customer):
        """
        Test database transaction rolls back on error.
        
        Verifies:
        - Partial data is not committed on error
        - Transaction atomicity works correctly
        """
        initial_count = UsageRecord.objects.count()
        
        try:
            with transaction.atomic():
                # Create valid usage record
                today = date.today()
                UsageRecord.objects.create(
                    customer=sample_customer,
                    billing_period_start=today,
                    billing_period_end=today + timedelta(days=30),
                    data_used_mb=Decimal('1000.00')
                )
                
                # Create invalid usage record (should fail)
                UsageRecord.objects.create(
                    customer=sample_customer,
                    billing_period_start=today,
                    billing_period_end=today - timedelta(days=30),  # Invalid!
                    data_used_mb=Decimal('1000.00')
                )
        except IntegrityError:
            pass
        
        # Verify no records were created (rollback occurred)
        assert UsageRecord.objects.count() == initial_count
    
    def test_update_customer_maintains_relationships(self, db, customer_with_full_data):
        """
        Test updating customer doesn't break relationships.
        
        Verifies:
        - Customer updates don't affect related records
        - Foreign key relationships remain valid
        """
        customer, account, usage_record = customer_with_full_data
        
        # Update customer
        customer.first_name = 'UpdatedName'
        customer.email = 'updated@test.com'
        customer.save()
        
        # Refresh related objects
        account.refresh_from_db()
        usage_record.refresh_from_db()
        
        # Verify relationships still intact
        assert account.customer_id == customer.id
        assert usage_record.customer_id == customer.id
        assert customer.account.id == account.id
    
    def test_null_values_in_optional_fields(self, db, sample_customer):
        """
        Test that optional fields can be null/blank.
        
        Verifies:
        - Phone number can be null
        - Usage limits can be null (unlimited)
        """
        # Customer without phone
        customer = Customer.objects.create(
            customer_code='NULL-001',
            first_name='No',
            last_name='Phone',
            email='nophone@test.com',
            phone_number=None
        )
        assert customer.phone_number is None
        
        # Usage with null limits
        today = date.today()
        usage = UsageRecord.objects.create(
            customer=customer,
            billing_period_start=today,
            billing_period_end=today + timedelta(days=30),
            data_used_mb=Decimal('5000.00'),
            data_limit_mb=None,  # Unlimited
            minutes_used=1000,
            minutes_limit=None,  # Unlimited
            sms_used=500,
            sms_limit=None  # Unlimited
        )
        assert usage.data_limit_mb is None
        assert usage.minutes_limit is None
        assert usage.sms_limit is None
