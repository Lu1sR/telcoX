"""
Unit tests for health check endpoint
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class HealthCheckTestCase(TestCase):
    """Test cases for health check endpoint"""

    def setUp(self):
        """Set up test client"""
        self.client = APIClient()

    def test_health_check_endpoint(self):
        """Test GET /api/health/ returns 200 and correct response"""
        response = self.client.get('/api/health/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'healthy')

    def test_health_check_response_structure(self):
        """Test health check response has expected structure"""
        response = self.client.get('/api/health/')
        
        self.assertIsInstance(response.data, dict)
        self.assertIn('status', response.data)
