from finance.models import PriceBase


def get_price_bases():
    return {
        pb.type: pb.price
        for pb in PriceBase.objects.all()
    }


def calculate_art_price(art, frame, passepartout, price_bases):
    width = art.width
    height = art.height
    distance = passepartout.distance

    return (
        price_bases["canvas"]
        + price_bases["fiber"]
        + price_bases["glue"]
        + (width * height) * price_bases["initial_print"]
        + price_bases["labor"]
        + (
            (width + 2 * distance) * (height + 2 * distance)
            - (width * height)
        ) * price_bases["passepartout"]
        + (width + height + 4 * distance) * 2 * frame.price
    )


def refresh_cart(cart):
    price_bases = get_price_bases()
    total_price = 0
    items = cart.items.select_related("art", "frame", "passepartout")

    for item in items:
        item.unit_price = calculate_art_price(
            item.art,
            item.frame,
            item.passepartout,
            price_bases
        )

        item.save(update_fields=["unit_price", "updated_at"])
        total_price += item.unit_price * item.quantity

    cart.total_price = total_price
    cart.save(update_fields=["total_price", "updated_at"])

    return cart