from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class VendorListCreateView(APIView):
    def get(self, request, format=None):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailView(APIView):
    def get_object(self, vendor_id):
        try:
            return Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, vendor_id, format=None):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_id, format=None):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id, format=None):
        vendor = self.get_object(vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








class PurchaseOrderListCreateView(APIView):
    def get(self, request, format=None):        
        vendor_name = request.query_params.get('vendor', None)
        print(vendor_name)

        if vendor_name:
            purchaseorder = PurchaseOrder.objects.filter(vendor__name__contains=vendor_name)
        else:
            purchaseorder = PurchaseOrder.objects.all()
            print(purchaseorder)


        serializer = PurchaseOrderSerializer(purchaseorder, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetailView(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            raise Http404

    def get(self, request, po_id, format=None):
        purchaseorder = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(purchaseorder)
        return Response(serializer.data)

    def put(self, request, po_id, format=None):
        purchaseorder = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(purchaseorder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id, format=None):
        purchaseorder = self.get_object(po_id)
        purchaseorder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
