"""
API Views for Customer and Account models.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Customer, Account
from .serializers import CustomerSerializer, AccountSerializer


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Customer model.
    Provides list and retrieve actions only (read-only).
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        """
        Optionally filter customers by search parameter.
        """
        queryset = Customer.objects.all()
        search = self.request.query_params.get('search', None)
        
        if search:
            queryset = queryset.filter(
                models.Q(customer_code__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'], url_path='account')
    def account(self, request, pk=None):
        """
        Get account information for a specific customer.
        GET /api/customers/{id}/account/
        """
        customer = self.get_object()
        
        try:
            account = customer.account
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response(
                {'error': 'No account found for this customer'},
                status=status.HTTP_404_NOT_FOUND
            )
