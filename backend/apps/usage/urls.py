"""
URL configuration for usage app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsageViewSet, CustomerUsageViewSet

router = DefaultRouter()
router.register(r'usage', UsageViewSet, basename='usage')

# Custom routes for customer usage overview
urlpatterns = [
    path('', include(router.urls)),
    path('customers/<int:pk>/usage/', 
         CustomerUsageViewSet.as_view({'get': 'retrieve'}), 
         name='customer-usage-overview'),
]
