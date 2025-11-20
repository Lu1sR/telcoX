"""
Unit tests for Customer API views
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from apps.customers.models import Customer, Account


class CustomerAPITestCase(TestCase):
    """Test cases for Customer API endpoints"""

    def setUp(self):
        """Set up test client and data"""
        self.client = APIClient()
        
        # Create test customers
        self.customer1 = Customer.objects.create(
            customer_code='CUST-001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='+1234567890'
        )
        self.customer2 = Customer.objects.create(
            customer_code='CUST-002',
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )
        
        # Create account for customer1
        self.account1 = Account.objects.create(
            customer=self.customer1,
            balance=Decimal('1000.00'),
            currency='USD',
            status='ACTIVE'
        )

    def test_get_customer_list(self):
        """Test GET /api/customers/ returns list of customers"""
        response = self.client.get('/api/customers/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify first customer data
        customer_data = response.data[0]
        self.assertEqual(customer_data['customer_code'], 'CUST-001')
        self.assertEqual(customer_data['first_name'], 'John')
        self.assertEqual(customer_data['last_name'], 'Doe')
        self.assertEqual(customer_data['email'], 'john.doe@example.com')

    def test_get_customer_detail(self):
        """Test GET /api/customers/{id}/ returns customer detail"""
        response = self.client.get(f'/api/customers/{self.customer1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_code'], 'CUST-001')
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['email'], 'john.doe@example.com')

    def test_get_customer_detail_not_found(self):
        """Test GET /api/customers/{id}/ with invalid ID returns 404"""
        response = self.client.get('/api/customers/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_customers_by_name(self):
        """Test searching customers by name"""
        response = self.client.get('/api/customers/?search=Jane')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Jane')

    def test_search_customers_by_email(self):
        """Test searching customers by email"""
        response = self.client.get('/api/customers/?search=john.doe@example.com')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'john.doe@example.com')

    def test_search_customers_by_customer_code(self):
        """Test searching customers by customer code"""
        response = self.client.get('/api/customers/?search=CUST-002')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['customer_code'], 'CUST-002')

    def test_customers_endpoint_is_read_only(self):
        """Test that POST/PUT/DELETE are not allowed on customers endpoint"""
        # Try POST
        response = self.client.post('/api/customers/', {
            'customer_code': 'CUST-003',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Try PUT
        response = self.client.put(f'/api/customers/{self.customer1.id}/', {
            'first_name': 'Updated'
        })
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Try DELETE
        response = self.client.delete(f'/api/customers/{self.customer1.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
