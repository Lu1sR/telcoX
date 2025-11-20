"""
Seed script to populate the database with test data.
Run with: python manage.py shell < scripts/seed_data.py
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.models import Customer, Account
from apps.usage.models import UsageRecord

def clear_data():
    """Clear existing data and reset auto-increment sequences."""
    print("Clearing existing data...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # Disable foreign key checks temporarily
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            
            # TRUNCATE tables (automatically resets AUTO_INCREMENT)
            # Order: child tables first, then parent tables
            cursor.execute("TRUNCATE TABLE usage_records;")
            cursor.execute("TRUNCATE TABLE accounts;")
            cursor.execute("TRUNCATE TABLE customers;")
            
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            
        print("✓ Data cleared and sequences reset to 1")
    except Exception as e:
        print(f"⚠ Warning: Could not clear data (tables may not exist yet): {e}")
        print("Continuing with seed...")

def create_customers():
    """Create sample customers."""
    print("\nCreating customers...")
    
    customers_data = [
        {
            'customer_code': 'CUST001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '+1234567890',
        },
        {
            'customer_code': 'CUST002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone_number': '+1234567891',
        },
        {
            'customer_code': 'CUST003',
            'first_name': 'Michael',
            'last_name': 'Johnson',
            'email': 'michael.johnson@example.com',
            'phone_number': '+1234567892',
        },
        {
            'customer_code': 'CUST004',
            'first_name': 'Emily',
            'last_name': 'Williams',
            'email': 'emily.williams@example.com',
            'phone_number': '+1234567893',
        },
        {
            'customer_code': 'CUST005',
            'first_name': 'David',
            'last_name': 'Brown',
            'email': 'david.brown@example.com',
            'phone_number': '+1234567894',
        },
        {
            'customer_code': 'CUST006',
            'first_name': 'Sarah',
            'last_name': 'Davis',
            'email': 'sarah.davis@example.com',
            'phone_number': '+1234567895',
        },
        {
            'customer_code': 'CUST007',
            'first_name': 'Robert',
            'last_name': 'Miller',
            'email': 'robert.miller@example.com',
            'phone_number': '+1234567896',
        },
        {
            'customer_code': 'CUST008',
            'first_name': 'Lisa',
            'last_name': 'Wilson',
            'email': 'lisa.wilson@example.com',
            'phone_number': '+1234567897',
        },
        {
            'customer_code': 'CUST009',
            'first_name': 'James',
            'last_name': 'Moore',
            'email': 'james.moore@example.com',
            'phone_number': '+1234567898',
        },
        {
            'customer_code': 'CUST010',
            'first_name': 'Maria',
            'last_name': 'Garcia',
            'email': 'maria.garcia@example.com',
            'phone_number': '+1234567899',
        },
    ]
    
    customers = []
    for data in customers_data:
        customer = Customer.objects.create(**data)
        customers.append(customer)
        print(f"  ✓ Created customer: {customer.customer_code}")
    
    return customers

def create_accounts(customers):
    """Create accounts for customers."""
    print("\nCreating accounts...")
    
    balances = [125.50, 89.75, 210.00, 45.25, 178.90, 92.60, 156.30, 203.45, 67.80, 134.20]
    statuses = ['ACTIVE'] * 8 + ['SUSPENDED', 'ACTIVE']
    
    accounts = []
    for i, customer in enumerate(customers):
        account = Account.objects.create(
            customer=customer,
            balance=Decimal(str(balances[i])),
            currency='USD',
            status=statuses[i]
        )
        accounts.append(account)
        print(f"  ✓ Created account for {customer.customer_code}: Balance ${account.balance}")
    
    return accounts

def create_usage_records(customers):
    """Create usage records for customers."""
    print("\nCreating usage records...")
    
    # Current billing period
    today = date.today()
    period_start = date(today.year, today.month, 1)
    
    # Calculate period end (last day of current month)
    if today.month == 12:
        period_end = date(today.year, 12, 31)
    else:
        period_end = date(today.year, today.month + 1, 1) - timedelta(days=1)
    
    usage_data = [
        {
            'data_used_mb': 4500.75,
            'data_limit_mb': 10240.00,  # 10 GB
            'minutes_used': 320,
            'minutes_limit': 500,
            'sms_used': 45,
            'sms_limit': 100,
        },
        {
            'data_used_mb': 8950.50,
            'data_limit_mb': 10240.00,
            'minutes_used': 485,
            'minutes_limit': 500,
            'sms_used': 92,
            'sms_limit': 100,
        },
        {
            'data_used_mb': 2100.25,
            'data_limit_mb': 5120.00,  # 5 GB
            'minutes_used': 150,
            'minutes_limit': 300,
            'sms_used': 28,
            'sms_limit': 50,
        },
        {
            'data_used_mb': 15360.00,
            'data_limit_mb': 20480.00,  # 20 GB
            'minutes_used': 720,
            'minutes_limit': 1000,
            'sms_used': 150,
            'sms_limit': 200,
        },
        {
            'data_used_mb': 6789.45,
            'data_limit_mb': 10240.00,
            'minutes_used': 412,
            'minutes_limit': 500,
            'sms_used': 67,
            'sms_limit': 100,
        },
        {
            'data_used_mb': 3456.80,
            'data_limit_mb': 10240.00,
            'minutes_used': 234,
            'minutes_limit': 500,
            'sms_used': 38,
            'sms_limit': 100,
        },
        {
            'data_used_mb': 9876.30,
            'data_limit_mb': 10240.00,
            'minutes_used': 467,
            'minutes_limit': 500,
            'sms_used': 89,
            'sms_limit': 100,
        },
        {
            'data_used_mb': 1234.56,
            'data_limit_mb': 5120.00,
            'minutes_used': 98,
            'minutes_limit': 300,
            'sms_used': 15,
            'sms_limit': 50,
        },
        {
            'data_used_mb': 18432.00,
            'data_limit_mb': 20480.00,
            'minutes_used': 892,
            'minutes_limit': 1000,
            'sms_used': 178,
            'sms_limit': 200,
        },
        {
            'data_used_mb': 5555.55,
            'data_limit_mb': 10240.00,
            'minutes_used': 333,
            'minutes_limit': 500,
            'sms_used': 55,
            'sms_limit': 100,
        },
    ]
    
    usage_records = []
    for i, customer in enumerate(customers):
        data = usage_data[i]
        usage = UsageRecord.objects.create(
            customer=customer,
            billing_period_start=period_start,
            billing_period_end=period_end,
            data_used_mb=Decimal(str(data['data_used_mb'])),
            data_limit_mb=Decimal(str(data['data_limit_mb'])),
            minutes_used=data['minutes_used'],
            minutes_limit=data['minutes_limit'],
            sms_used=data['sms_used'],
            sms_limit=data['sms_limit'],
        )
        usage_records.append(usage)
        
        data_pct = usage.get_data_used_percentage()
        minutes_pct = usage.get_minutes_used_percentage()
        print(f"  ✓ Created usage for {customer.customer_code}: "
              f"Data {data_pct}%, Minutes {minutes_pct}%")
    
    return usage_records

def main():
    """Main function to seed all data."""
    print("=" * 60)
    print("TelcoX Database Seeding Script")
    print("=" * 60)
    
    try:
        clear_data()
        customers = create_customers()
        accounts = create_accounts(customers)
        usage_records = create_usage_records(customers)
        
        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully!")
        print(f"  - Customers: {len(customers)}")
        print(f"  - Accounts: {len(accounts)}")
        print(f"  - Usage Records: {len(usage_records)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
