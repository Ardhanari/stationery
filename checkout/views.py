from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from accounts.forms import ShippingAddressForm # model to store address in the database for later use? 
from django.conf import settings
from django.utils import timezone
from products.models import Product
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def checkout(request):
    if request.method == "POST":
        shipping_address_form = ShippingAddressForm(request.POST) 
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        user = request.user

        if shipping_address_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.user = user
            # ship_ad = order
            order.save()

            shipping_address = shipping_address_form.save(commit=False)
            shipping_address.user = user
            shipping_address.save()

            # shipping_adress_form = ""
            # shipping_address_form.deepcopy(order_form)
            # shipping_address = shipping_address_form.save(commit=False)
            # shipping_address.user = user
            # shipping_address.save()

            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                order_line_item.save()
            
            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id']
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
            
            if customer.paid:
                messages.success(request, "You have successfully paid for the order")
                for id, quantity in cart.items():
                    product = get_object_or_404(Product, pk=id)
                    product.quantity -= quantity
                    product.save()
                request.session['cart'] = {}
                return redirect(reverse('allproducts'))
            else:
                messages.error(request, "Unable to take payment at this time")
                return redirect(reverse('checkout'))
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        shipping_address_form = ShippingAddressForm() # if shipping address exists in the database - prepopulate, if not leave blank
    
    return render(request, "checkout.html", {"shipping_form": shipping_address_form, "order_form": order_form, "payment_form": payment_form, "publishable": settings.STRIPE_PUBLISHABLE})
