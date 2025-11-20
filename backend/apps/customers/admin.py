"""
Django admin configuration for Customer and Account models.
"""
from django.contrib import admin
from .models import Customer, Account


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_code', 'first_name', 'last_name', 'email', 'phone_number', 'created_at']
    search_fields = ['customer_code', 'first_name', 'last_name', 'email']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['customer', 'balance', 'currency', 'status', 'created_at']
    search_fields = ['customer__customer_code', 'customer__email']
    list_filter = ['status', 'currency', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def customer(self, obj):
        return obj.customer.customer_code
    customer.short_description = 'Customer'
