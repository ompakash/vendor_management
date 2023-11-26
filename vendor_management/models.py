from django.db import models
from django.db.models import Count, Avg
from django.utils import timezone

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def update_performance_metrics(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')

        # On-Time Delivery Rate
        completed_on_time = completed_pos.filter(delivery_date__lte=timezone.now())
        self.on_time_delivery_rate = (completed_on_time.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0.0

        # Quality Rating Average
        completed_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        self.quality_rating_avg = completed_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0

        # Average Response Time
        acknowledged_pos = completed_pos.filter(acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]
        self.average_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0.0


        # Fulfilment Rate
        successful_fulfillment = completed_pos.exclude(status='completed_with_issues')
        self.fulfillment_rate = (successful_fulfillment.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0.0

        self.save()


    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vendor.update_performance_metrics()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.vendor.update_performance_metrics()

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
