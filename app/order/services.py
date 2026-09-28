from django.db import transaction
from django.db.models import F
from django.utils import timezone

from accounts.models import Address
from Cart.models import Cart
from Cart.services import refresh_cart, get_price_bases
from finance.models import DiscountCode

from .models import Order, OrderItem


def get_user_address(user, address_id):
    try:
        return Address.objects.get(pk=address_id, user=user)
    except Address.DoesNotExist:
        raise ValueError("آدرس انتخاب‌شده یافت نشد")

def get_shipping_price(destination, price_bases=None):
    price_bases = price_bases or get_price_bases()
    if destination == Order.Destination.TEHRAN:
        return price_bases["shipping_tehran"]
    return price_bases["shipping_other"]


def get_valid_discount_code(code):
    try:
        discount = DiscountCode.objects.get(code=code)
    except DiscountCode.DoesNotExist:
        raise ValueError("کد تخفیف معتبر نیست")

    if discount.expires_at <= timezone.now():
        raise ValueError("کد تخفیف منقضی شده است")

    if discount.used_count >= discount.quantity:
        raise ValueError("ظرفیت استفاده از این کد تخفیف تمام شده است")

    return discount


def calculate_discount_amount(discount, items_price):
    if discount.type == DiscountCode.DiscountType.PERCENTAGE:
        return items_price * discount.amount // 100
    else:
        return items_price - discount.amount


@transaction.atomic
def create_order_from_cart(user, address_id, destination, discount_code_str=None):
    cart = Cart.objects.select_for_update().filter(user=user).first()
    if cart is None or not cart.items.exists():
        raise ValueError("سبد خرید شما خالی است")

    refresh_cart(cart)
    items = list(cart.items.select_related("art", "frame", "passepartout"))

    address = get_user_address(user, address_id)
    price_bases = get_price_bases()
    shipping_price = get_shipping_price(destination, price_bases)
    items_price = sum(item.unit_price * item.quantity for item in items)

    discount = None
    discount_amount = 0
    if discount_code_str:
        discount = get_valid_discount_code(discount_code_str)
        discount_amount = calculate_discount_amount(discount, items_price)

    order = Order(
        user=user,
        address=address,
        destination=destination,
        discount_code=discount,
        items_price=items_price,
        shipping_price=shipping_price,
        discount_amount=discount_amount,
    )
    order.total_price = items_price + shipping_price - discount_amount
    order.save()

    OrderItem.objects.bulk_create([
        OrderItem(
            order=order,
            art=item.art,
            frame=item.frame,
            passepartout=item.passepartout,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        for item in items
    ])

    if discount:
        DiscountCode.objects.filter(pk=discount.pk).update(used_count=F("used_count") + 1)

    cart.delete()

    return order