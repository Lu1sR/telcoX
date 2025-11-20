"""
Unit tests for Customer and Account models
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from apps.customers.models import Customer, Account


class CustomerModelTestCase(TestCase):
    """Test cases for Customer model"""

    def setUp(self):
        """Set up test data"""
        self.customer_data = {
            'customer_code': 'CUST-001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '+1234567890'
        }

    def test_create_customer_with_valid_data(self):
        """Test creating a customer with valid data"""
        customer = Customer.objects.create(**self.customer_data)
        
        self.assertEqual(customer.customer_code, 'CUST-001')
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.last_name, 'Doe')
        self.assertEqual(customer.email, 'john.doe@example.com')
        self.assertEqual(customer.phone_number, '+1234567890')
        self.assertIsNotNone(customer.created_at)
        self.assertIsNotNone(customer.updated_at)

    def test_create_customer_without_phone_number(self):
        """Test creating a customer without optional phone number"""
        data = self.customer_data.copy()
        data.pop('phone_number')
        customer = Customer.objects.create(**data)
        
        self.assertIsNone(customer.phone_number)
        self.assertEqual(customer.email, 'john.doe@example.com')

    def test_customer_str_representation(self):
        """Test customer string representation"""
        customer = Customer.objects.create(**self.customer_data)
        expected = f"{customer.first_name} {customer.last_name} ({customer.customer_code})"
        self.assertEqual(str(customer), expected)

    def test_customer_code_uniqueness(self):
        """Test that customer_code must be unique"""
        Customer.objects.create(**self.customer_data)
        
        # Try to create another customer with same code
        with self.assertRaises(Exception):  # IntegrityError
            Customer.objects.create(**self.customer_data)

    def test_email_uniqueness(self):
        """Test that email must be unique"""
        Customer.objects.create(**self.customer_data)
        
        # Try to create another customer with same email
        data = self.customer_data.copy()
        data['customer_code'] = 'CUST-002'
        with self.assertRaises(Exception):  # IntegrityError
            Customer.objects.create(**data)


class AccountModelTestCase(TestCase):
    """Test cases for Account model"""

    def setUp(self):
        """Set up test data"""
        self.customer = Customer.objects.create(
            customer_code='CUST-001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )

    def test_create_account_with_valid_data(self):
        """Test creating an account with valid data"""
        account = Account.objects.create(
            customer=self.customer,
            balance=Decimal('1000.00'),
            currency='USD',
            status='ACTIVE'
        )
        
        self.assertEqual(account.customer, self.customer)
        self.assertEqual(account.balance, Decimal('1000.00'))
        self.assertEqual(account.currency, 'USD')
        self.assertEqual(account.status, 'ACTIVE')
        self.assertIsNotNone(account.created_at)
        self.assertIsNotNone(account.updated_at)

    def test_account_default_values(self):
        """Test account default values"""
        account = Account.objects.create(
            customer=self.customer
        )
        
        self.assertEqual(account.balance, Decimal('0.00'))
        self.assertEqual(account.currency, 'USD')
        self.assertEqual(account.status, 'ACTIVE')

    def test_account_str_representation(self):
        """Test account string representation"""
        account = Account.objects.create(
            customer=self.customer,
            balance=Decimal('500.00')
        )
        expected = f"Account for {self.customer.customer_code} - Balance: 500.00 USD"
        self.assertEqual(str(account), expected)

    def test_account_status_choices(self):
        """Test account status choices"""
        valid_statuses = ['ACTIVE', 'SUSPENDED', 'CLOSED']
        
        for i, status in enumerate(valid_statuses):
            customer = Customer.objects.create(
                customer_code=f'CUST-STATUS-{i}',
                first_name='Test',
                last_name='User',
                email=f'test{i}@example.com'
            )
            account = Account.objects.create(
                customer=customer,
                status=status
            )
            self.assertEqual(account.status, status)

    def test_customer_can_have_only_one_account(self):
        """Test that a customer can have only one account (OneToOne relationship)"""
        account = Account.objects.create(
            customer=self.customer,
            balance=Decimal('1000.00')
        )
        
        # Verify the account is linked
        self.assertEqual(self.customer.account, account)
        self.assertEqual(account.customer, self.customer)
        
        # Attempting to create a second account for same customer should fail
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Account.objects.create(
                customer=self.customer,
                balance=Decimal('500.00')
            )

    def test_account_cascade_delete(self):
        """Test that deleting a customer deletes associated account"""
        Account.objects.create(customer=self.customer)
        
        customer_id = self.customer.id
        self.assertEqual(Account.objects.filter(customer_id=customer_id).count(), 1)
        
        self.customer.delete()
        
        self.assertEqual(Account.objects.filter(customer_id=customer_id).count(), 0)

    def test_negative_balance_allowed(self):
        """Test that negative balance is allowed (overdraft)"""
        account = Account.objects.create(
            customer=self.customer,
            balance=Decimal('-50.00')
        )
        self.assertEqual(account.balance, Decimal('-50.00'))
