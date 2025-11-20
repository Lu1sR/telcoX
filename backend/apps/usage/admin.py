"""
Django admin configuration for UsageRecord model.
"""
from django.contrib import admin
from .models import UsageRecord


@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display = [
        'customer_code',
        'billing_period_start',
        'billing_period_end',
        'data_used_mb',
        'data_limit_mb',
        'minutes_used',
        'minutes_limit',
        'created_at',
    ]
    search_fields = [
        'customer__customer_code',
        'customer__email',
        'customer__first_name',
        'customer__last_name',
    ]
    list_filter = ['billing_period_start', 'billing_period_end', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-billing_period_end', '-created_at']
    
    def customer_code(self, obj):
        return obj.customer.customer_code
    customer_code.short_description = 'Customer Code'
    customer_code.admin_order_field = 'customer__customer_code'
