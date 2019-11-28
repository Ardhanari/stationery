from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from accounts.forms import ShippingAddressForm # model to store address in the database for later use?
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
            shipping_address.id = ShippingAddress.objects.get(user=user).id
            shipping_address.save()
            messages.success(request, "Address saved")
            return redirect(reverse('checkout'))

        else: 
            # shipping_address = shipping_address_form.save(commit=False)
            # shipping_address.user = user
            # shipping_address.save()
            print("BOOOO")

            messages.error(request, "There was a problem with saving your data. Please make sure all fields are filled correctly.")
            return redirect(reverse('addressdetails'))

    else:
        try:
            address_exists = ShippingAddress.objects.get(user=user)
            print("ok")
            shipping_address_form = ShippingAddressForm(initial={'full_name': address_exists.full_name, 'company': address_exists.company, 
                                                                'street_address1': address_exists.street_address1, 'street_address2': address_exists.street_address2,
                                                                'postcode': address_exists.postcode, 'town_or_city': address_exists.town_or_city, 
                                                                'county': address_exists.country, 'country': address_exists.country, 
                                                                'phone_number': address_exists.phone_number
                                                                }, auto_id=False)

        except Exception as e:
            print('%s (%s)') % (e.message, type(e))
            print("not ok")
            shipping_address_form = ShippingAddressForm() 

    return render(request, "address_details.html", {"shipping_form": shipping_address_form})

@login_required()
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        user = request.user

        if payment_form.is_valid():

            shipping_address = ShippingAddress.objects.get(user=user)
            print(shipping_address)
            
            order = order_form.save(commit=False)
            order.address_id = shipping_address.id
            order.date = timezone.now()
            order.user = user
            order.save()

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
        user = request.user
        shipping_address_form = ShippingAddress.objects.get(user=user) # if shipping address exists in the database - prepopulate, if not leave blank
        order_form = OrderForm(initial={'phone_number': shipping_address_form.phone_number})
        # try: 
        #     shipping_address_form = ShippingAddress.objects.get(user=user) # if shipping address exists in the database - prepopulate, if not leave blank
        # except: 
        #     shipping_address_form = ShippingAddress()
        payment_form = MakePaymentForm()    
    
    return render(request, "checkout.html", {"order_form": order_form, "payment_form": payment_form, "publishable": settings.STRIPE_PUBLISHABLE})
