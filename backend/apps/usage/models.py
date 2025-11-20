"""
Usage model for tracking customer consumption data.
"""
from django.db import models
from django.core.validators import MinValueValidator
from apps.customers.models import Customer


class UsageRecord(models.Model):
    """
    Model representing usage/consumption data for a customer's billing period.
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='usage_records'
    )
    billing_period_start = models.DateField(
        help_text="Start date of billing cycle"
    )
    billing_period_end = models.DateField(
        help_text="End date of billing cycle"
    )
    
    # Data usage
    data_used_mb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Data consumed in megabytes"
    )
    data_limit_mb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Data allowance in megabytes (NULL = unlimited)"
    )
    
    # Voice minutes usage
    minutes_used = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Voice minutes consumed"
    )
    minutes_limit = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Minutes allowance (NULL = unlimited)"
    )
    
    # SMS usage (optional for future use)
    sms_used = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="SMS count"
    )
    sms_limit = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="SMS allowance (NULL = unlimited)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usage_records'
        ordering = ['-billing_period_end']
        indexes = [
            models.Index(fields=['customer', '-billing_period_end']),
            models.Index(fields=['billing_period_start', 'billing_period_end']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(billing_period_end__gte=models.F('billing_period_start')),
                name='billing_period_dates_check'
            ),
        ]

    def __str__(self):
        try:
            account = self.customer.account
            return f"Usage for {account} ({self.billing_period_start} to {self.billing_period_end})"
        except:
            return f"Usage for {self.customer.customer_code} ({self.billing_period_start} to {self.billing_period_end})"

    @property
    def data_used_percentage(self):
        """Calculate percentage of data used."""
        if self.data_limit_mb and self.data_limit_mb > 0:
            return round((float(self.data_used_mb) / float(self.data_limit_mb)) * 100, 2)
        return None

    def get_data_used_percentage(self):
        """Calculate percentage of data used (backward compatibility)."""
        return self.data_used_percentage

    @property
    def minutes_used_percentage(self):
        """Calculate percentage of minutes used."""
        if self.minutes_limit and self.minutes_limit > 0:
            return round((self.minutes_used / self.minutes_limit) * 100, 2)
        return None

    def get_minutes_used_percentage(self):
        """Calculate percentage of minutes used (backward compatibility)."""
        return self.minutes_used_percentage

    @property
    def sms_used_percentage(self):
        """Calculate percentage of SMS used."""
        if self.sms_limit and self.sms_limit > 0:
            return round((self.sms_used / self.sms_limit) * 100, 2)
        return None

    def get_sms_used_percentage(self):
        """Calculate percentage of SMS used (backward compatibility)."""
        return self.sms_used_percentage
