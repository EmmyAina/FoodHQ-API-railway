import uuid
from datetime import datetime, timedelta, timezone
from business.models import VendorInformation
from authentication.models import User
from django.db import models


class OrderInformation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorInformation, on_delete=models.CASCADE)
    amount = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255)
    order_detail = models.TextField(max_length=5000)
    message = models.TextField(max_length=10000)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, )
    payment_method = models.CharField(max_length=10)
    trx_ref = models.CharField(max_length=50, blank=True)
    order_id = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return f'{self.id} {self.user.username} => {self.vendor.name} => {self.amount}'

    class Meta:
        ordering = ("-date", )
        verbose_name_plural = "Order Information"

    def complete_order(self):
        self.completed = True
        self.save()
