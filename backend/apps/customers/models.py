"""
Customer and Account models for TelcoX.
"""
from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Customer(models.Model):
    """
    Customer model representing a TelcoX customer.
    """
    customer_code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique business customer code"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()]
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['customer_code']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.customer_code})"

    def get_full_name(self):
        """Returns the customer's full name."""
        return f"{self.first_name} {self.last_name}"


class Account(models.Model):
    """
    Account model representing a customer's billing account.
    One-to-one relationship with Customer.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('CLOSED', 'Closed'),
    ]

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='account'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Current account balance"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="ISO 4217 currency code"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=-1000.00),
                name='balance_minimum_check'
            )
        ]

    def __str__(self):
        return f"Account for {self.customer.customer_code} - Balance: {self.balance} {self.currency}"
