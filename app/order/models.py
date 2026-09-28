from django.db import models
from django.db.models import F
from django.utils import timezone

from accounts.models import User, Address
from art.models import Art, Frame, Passepartout
from finance.models import DiscountCode


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Destination(models.TextChoices):
        TEHRAN = "tehran", "Tehran"
        OTHER = "other", "Other"

    CANCELLABLE_STATUSES = {Status.PENDING, Status.PAID}

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    destination = models.CharField(max_length=10, choices=Destination.choices)

    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")

    items_price = models.PositiveBigIntegerField(default=0)
    shipping_price = models.PositiveBigIntegerField(default=0)
    discount_amount = models.PositiveBigIntegerField(default=0)
    total_price = models.PositiveBigIntegerField(default=0)

    paid_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def release_discount_code(self):
        if self.discount_code_id:
            DiscountCode.objects.filter(pk=self.discount_code_id).update(
                used_count=F("used_count") - 1
            )

    def mark_as_paid(self):
        if self.status != self.Status.PENDING:
            raise ValueError("فقط سفارش در انتظار پرداخت را می‌توان پرداخت‌شده کرد")
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at", "updated_at"])

    def cancel(self):
        if self.status not in self.CANCELLABLE_STATUSES:
            raise ValueError("این سفارش در وضعیت فعلی قابل لغو نیست")
        self.release_discount_code()
        self.status = self.Status.CANCELLED
        self.cancelled_at = timezone.now()
        self.save(update_fields=["status", "cancelled_at", "updated_at"])

    def mark_as_shipped(self):
        if self.status != self.Status.PAID:
            raise ValueError("فقط سفارش پرداخت‌شده را می‌توان ارسال کرد")
        self.status = self.Status.SHIPPED
        self.save(update_fields=["status", "updated_at"])

    def mark_as_completed(self):
        if self.status != self.Status.SHIPPED:
            raise ValueError("فقط سفارش ارسال‌شده را می‌توان تکمیل کرد")
        self.status = self.Status.COMPLETED
        self.save(update_fields=["status", "updated_at"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    art = models.ForeignKey(Art, on_delete=models.PROTECT, related_name="order_items")
    frame = models.ForeignKey(Frame, on_delete=models.PROTECT, related_name="order_items")
    passepartout = models.ForeignKey(Passepartout, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveBigIntegerField()