"""
Business logic services for usage data.
"""
from apps.customers.models import Customer, Account
from apps.customers.serializers import CustomerSerializer, AccountSerializer
from .models import UsageRecord
from .serializers import UsageRecordSerializer


class UsageService:
    """Service class for usage-related business logic."""
    
    @staticmethod
    def get_customer_usage_overview(customer_id):
        """
        Get combined customer, account, and current usage data.
        
        Args:
            customer_id: ID of the customer
            
        Returns:
            dict: Dictionary containing serialized customer, account, and usage data
            None: If customer not found
        """
        # Get customer (return None if not found)
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return None
        
        # Get account (may not exist)
        try:
            account = customer.account
        except Account.DoesNotExist:
            account = None
        
        # Get most recent usage record for current billing period
        usage = UsageRecord.objects.filter(
            customer=customer
        ).order_by('-billing_period_end').first()
        
        return {
            'customer': CustomerSerializer(customer).data if customer else None,
            'account': AccountSerializer(account).data if account else None,
            'usage': UsageRecordSerializer(usage).data if usage else None,
        }
