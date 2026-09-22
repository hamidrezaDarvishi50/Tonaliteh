from django.db import models

# Create your models here.

class PriceBase(models.Model):

    class PriceType(models.TextChoices):
        CANVAS = "canvas", "Canvas"
        FIBER = "fiber", "Fiber"
        GLUE = "glue", "Glue"
        INITIAL_PRINT = "initial_print", "Initial Print"
        PASSEPARTOUT = "passepartout", "Passepartout"
        LABOR = "labor", "Labor"
        SHIPPING_TEHRAN = "shipping_tehran", "Shipping Tehran"
        SHIPPING_OTHER = "shipping_other", "Shipping Other"

    type = models.CharField(max_length=30, choices=PriceType.choices, unique=True)
    price = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

class DiscountCode(models.Model):

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed"

    type = models.CharField(max_length=20, choices=DiscountType.choices)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    expires_at = models.DateTimeField()
    quantity = models.PositiveIntegerField()
    used_count = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)