from django.shortcuts import get_object_or_404
from products.models import Product

def cart_content(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total_for_products = 0 # price for products without shipping
    product_count = 0
    shipping_rate = 15
    total = 0 # final price of products and shipping 

    for id, quantity in cart.items():
        product = get_object_or_404(Product, pk=id)
        # adjust the quantity of the product in cart so it's never more than available in stock
        if quantity > product.quantity:
            quantity = product.quantity
        else: 
            quantity = quantity
        total_for_products += quantity * product.price
        product_count += quantity
        total = total_for_products + shipping_rate
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})

    return {'cart_items': cart_items, 'total_for_products': total_for_products, 'total': total, 'product_count': product_count, 'shipping_rate': shipping_rate}