"""
Shared fixtures for integration tests.

These fixtures provide common test data and setup for integration tests.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord


@pytest.fixture
def sample_customer(db):
    """
    Create a sample customer for testing.
    
    Returns:
        Customer: A customer instance with basic information
    """
    return Customer.objects.create(
        customer_code='TEST-001',
        first_name='John',
        last_name='Doe',
        email='john.doe@test.com',
        phone_number='+14155551234'
    )


@pytest.fixture
def sample_account(db, sample_customer):
    """
    Create a sample account linked to sample_customer.
    
    Returns:
        Account: An account instance with balance and status
    """
    return Account.objects.create(
        customer=sample_customer,
        balance=Decimal('1250.00'),
        currency='USD',
        status='ACTIVE'
    )


@pytest.fixture
def sample_usage_record(db, sample_customer):
    """
    Create a sample usage record with typical usage data.
    
    Returns:
        UsageRecord: A usage record with data, minutes, and SMS usage
    """
    today = date.today()
    return UsageRecord.objects.create(
        customer=sample_customer,
        billing_period_start=today.replace(day=1),
        billing_period_end=today + timedelta(days=30),
        data_used_mb=Decimal('5120.00'),
        data_limit_mb=Decimal('10240.00'),
        minutes_used=250,
        minutes_limit=500,
        sms_used=50,
        sms_limit=100
    )


@pytest.fixture
def customer_with_full_data(db):
    """
    Create a customer with account and usage record in one fixture.
    
    Returns:
        tuple: (customer, account, usage_record)
    """
    customer = Customer.objects.create(
        customer_code='FULL-001',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@test.com',
        phone_number='+14155559876'
    )
    
    account = Account.objects.create(
        customer=customer,
        balance=Decimal('2500.00'),
        currency='USD',
        status='ACTIVE'
    )
    
    today = date.today()
    usage_record = UsageRecord.objects.create(
        customer=customer,
        billing_period_start=today.replace(day=1),
        billing_period_end=today + timedelta(days=30),
        data_used_mb=Decimal('7680.00'),
        data_limit_mb=Decimal('10240.00'),
        minutes_used=375,
        minutes_limit=500,
        sms_used=75,
        sms_limit=100
    )
    
    return customer, account, usage_record


@pytest.fixture
def multiple_customers(db):
    """
    Create multiple customers for list/search testing.
    
    Returns:
        list: List of 5 customer instances
    """
    customers = []
    for i in range(5):
        customer = Customer.objects.create(
            customer_code=f'MULTI-{i:03d}',
            first_name=f'User{i}',
            last_name=f'Test{i}',
            email=f'user{i}@test.com',
            phone_number=f'+1415555{i:04d}'
        )
        customers.append(customer)
    
    return customers


@pytest.fixture
def customer_without_account(db):
    """
    Create a customer without an associated account.
    
    Returns:
        Customer: Customer instance with no account
    """
    return Customer.objects.create(
        customer_code='NO-ACCT-001',
        first_name='Bob',
        last_name='Wilson',
        email='bob.wilson@test.com'
    )


@pytest.fixture
def customer_with_unlimited_plan(db):
    """
    Create a customer with unlimited usage (no limits).
    
    Returns:
        tuple: (customer, account, usage_record)
    """
    customer = Customer.objects.create(
        customer_code='UNLIM-001',
        first_name='Alice',
        last_name='Johnson',
        email='alice.johnson@test.com'
    )
    
    account = Account.objects.create(
        customer=customer,
        balance=Decimal('5000.00'),
        status='ACTIVE'
    )
    
    today = date.today()
    usage_record = UsageRecord.objects.create(
        customer=customer,
        billing_period_start=today.replace(day=1),
        billing_period_end=today + timedelta(days=30),
        data_used_mb=Decimal('50000.00'),
        data_limit_mb=None,  # Unlimited
        minutes_used=1000,
        minutes_limit=None,  # Unlimited
        sms_used=500,
        sms_limit=None  # Unlimited
    )
    
    return customer, account, usage_record


@pytest.fixture
def customer_with_high_usage(db):
    """
    Create a customer with usage exceeding 90% of limits.
    
    Returns:
        tuple: (customer, account, usage_record)
    """
    customer = Customer.objects.create(
        customer_code='HIGH-001',
        first_name='Charlie',
        last_name='Brown',
        email='charlie.brown@test.com'
    )
    
    account = Account.objects.create(
        customer=customer,
        balance=Decimal('100.00'),
        status='ACTIVE'
    )
    
    today = date.today()
    usage_record = UsageRecord.objects.create(
        customer=customer,
        billing_period_start=today.replace(day=1),
        billing_period_end=today + timedelta(days=30),
        data_used_mb=Decimal('9500.00'),  # 92.77% of 10240
        data_limit_mb=Decimal('10240.00'),
        minutes_used=480,  # 96% of 500
        minutes_limit=500,
        sms_used=95,  # 95% of 100
        sms_limit=100
    )
    
    return customer, account, usage_record
