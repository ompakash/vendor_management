# vendor_management/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),

    path('purchase_order/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_order/<int:po_id>/', PurchaseOrderDetailView.as_view(), name='purchase-order'),
]
  