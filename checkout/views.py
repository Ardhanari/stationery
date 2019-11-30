from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from accounts.forms import ShippingAddressForm
from accounts.models import ShippingAddress 
from django.conf import settings
from django.utils import timezone
from products.models import Product
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def address_details(request):
    user = request.user

    if request.method == "POST":
        shipping_address_form = ShippingAddressForm(request.POST) 

        if shipping_address_form.is_valid():
            shipping_address = shipping_address_form.save(commit=False)
            shipping_address.user = user
            try:
                shipping_address.id = ShippingAddress.objects.get(user=user).id
            except:
                pass
            shipping_address.save()
            messages.success(request, "Address saved")
            return redirect(reverse('checkout'))

        else: 

            messages.error(request, "There was a problem with saving your data. Please make sure all fields are filled correctly.")
            return redirect(reverse('addressdetails'))

    else:
        try:
            address_exists = ShippingAddress.objects.get(user=user)
            # prepopulates form with existing data
            shipping_address_form = ShippingAddressForm(initial={'full_name': address_exists.full_name, 'company': address_exists.company, 
                                                                'street_address1': address_exists.street_address1, 'street_address2': address_exists.street_address2,
                                                                'postcode': address_exists.postcode, 'town_or_city': address_exists.town_or_city, 
                                                                'county': address_exists.country, 'country': address_exists.country, 
                                                                'phone_number': address_exists.phone_number
                                                                }, auto_id=False)

        except:
            shipping_address_form = ShippingAddressForm() 

    return render(request, "address_details.html", {"shipping_form": shipping_address_form})

@login_required()
def checkout(request):
    """
    if form is posted and valid sends allows stripe to handle the payment 
    """
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        user = request.user

        if payment_form.is_valid():

            shipping_address = ShippingAddress.objects.get(user=user)
            
            order = order_form.save(commit=False)
            order.address_id = shipping_address.id
            order.date = timezone.now()
            order.user = user
            order.save()

            cart = request.session.get('cart', {})
            total_for_products = 0
            shipping_rate = 15
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total_for_products += quantity * product.price
                total = total_for_products + shipping_rate
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
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        user = request.user
        shipping_address_form = ShippingAddress.objects.get(user=user) 
        order_form = OrderForm(initial={'phone_number': shipping_address_form.phone_number})
        payment_form = MakePaymentForm()    
    
    return render(request, "checkout.html", {"order_form": order_form, "payment_form": payment_form, "publishable": settings.STRIPE_PUBLISHABLE})
