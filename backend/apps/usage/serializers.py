"""
Serializers for UsageRecord model and combined customer usage data.
"""
from rest_framework import serializers
from .models import UsageRecord
from apps.customers.serializers import CustomerSerializer, AccountSerializer


class UsageRecordSerializer(serializers.ModelSerializer):
    """Serializer for UsageRecord model with calculated percentages."""
    
    data_used_percentage = serializers.SerializerMethodField()
    minutes_used_percentage = serializers.SerializerMethodField()
    sms_used_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = UsageRecord
        fields = [
            'id',
            'billing_period_start',
            'billing_period_end',
            'data_used_mb',
            'data_limit_mb',
            'data_used_percentage',
            'minutes_used',
            'minutes_limit',
            'minutes_used_percentage',
            'sms_used',
            'sms_limit',
            'sms_used_percentage',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_data_used_percentage(self, obj):
        """Get percentage of data used."""
        return obj.get_data_used_percentage()
    
    def get_minutes_used_percentage(self, obj):
        """Get percentage of minutes used."""
        return obj.get_minutes_used_percentage()
    
    def get_sms_used_percentage(self, obj):
        """Get percentage of SMS used."""
        return obj.get_sms_used_percentage()


class CustomerUsageOverviewSerializer(serializers.Serializer):
    """
    Combined serializer for customer, account, and current usage data.
    This is the main response for the "My Usage" screen.
    
    Note: This serializer expects pre-serialized data from UsageService.
    """
    customer = serializers.DictField(allow_null=True)
    account = serializers.DictField(allow_null=True)
    usage = serializers.DictField(allow_null=True)
    
    def to_representation(self, instance):
        """
        Pass through the already-serialized data from UsageService.
        """
        return {
            'customer': instance.get('customer'),
            'account': instance.get('account'),
            'usage': instance.get('usage'),
        }
