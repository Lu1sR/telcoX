"""
Serializers for Customer and Account models.
"""
from rest_framework import serializers
from .models import Customer, Account


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'customer_code',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account model."""
    
    class Meta:
        model = Account
        fields = [
            'id',
            'balance',
            'currency',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
