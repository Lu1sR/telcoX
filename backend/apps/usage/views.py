"""
API Views for Usage data.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.customers.models import Customer
from .models import UsageRecord
from .serializers import UsageRecordSerializer, CustomerUsageOverviewSerializer
from .services import UsageService


class UsageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for UsageRecord model.
    Provides list and retrieve actions only (read-only).
    """
    queryset = UsageRecord.objects.all()
    serializer_class = UsageRecordSerializer
    
    def get_queryset(self):
        """
        Optionally filter usage records by customer.
        """
        queryset = UsageRecord.objects.select_related('customer')
        customer_id = self.request.query_params.get('customer_id', None)
        
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        return queryset


class CustomerUsageViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving combined customer usage overview.
    This is the main endpoint for the "My Usage" screen.
    """
    
    def retrieve(self, request, pk=None):
        """
        Get complete usage overview for a customer.
        GET /api/customers/{id}/usage/
        
        Returns combined customer info, account balance, and current usage.
        """
        try:
            usage_data = UsageService.get_customer_usage_overview(pk)
            
            if usage_data is None:
                return Response(
                    {'error': f'Customer with id {pk} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CustomerUsageOverviewSerializer(usage_data)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
