from django.db import models

# Create your models here.
from django.db import models

from accounts.models import User
from art.models import Art, Frame, Passepartout


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="cart")
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    art = models.ForeignKey(Art, on_delete=models.PROTECT, related_name="cart_items")
    frame = models.ForeignKey(Frame, on_delete=models.PROTECT, related_name="cart_items")
    passepartout = models.ForeignKey(Passepartout, on_delete=models.PROTECT, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'art', 'frame', 'passepartout'],
                name='unique_cart_item_configuration'
            )
        ]