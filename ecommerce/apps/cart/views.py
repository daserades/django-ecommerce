from django.shortcuts import render,redirect
from .cart import Cart
from django.conf import settings
from django.contrib import messages
from .forms import CheckoutForm
import traceback
from apps.customer.models import Customer
from apps.order.utilities import checkout, notify_customer, notify_vendor
from django.contrib.auth.decorators import login_required
from apps.core.decorators import unauthenticated_user,allowed_users,admin_only,customer_required
import stripe
@customer_required
def cart_detail(request):
    cart=Cart(request)
    customer=Customer.objects.get(user_id=request.user.id)
    flag=True
    form = CheckoutForm(request.POST)
    if request.method=='POST':
        
        print(form.is_valid())
        if form.is_valid():
            stripe.api_key= settings.STRIPE_SECRET_KEY

            stripe_token=form.cleaned_data['stripe_token']
            try:
                charge = stripe.Charge.create(
                    amount=int(cart.get_total_cost()*100),
                    currency='USD',
                    description='Django ecommerce Price',
                    source=stripe_token
                )
                order = checkout(request,customer, cart.get_total_cost())
                cart.clear()
                notify_customer(order)
                notify_vendor(order)
                        
                return redirect('success')
            except Exception as e:
                print(e)
                return redirect('problem')
                messages.error(request,'Your order could not be created')
        else:
            form = CheckoutForm()
    
    
    if flag:
        remove_from_cart= request.GET.get('remove_from_cart', '')
        change_quantity = request.GET.get('change_quantity','')
        quantity=request.GET.get('quantity',0)

        if remove_from_cart:
            cart.remove(remove_from_cart)
            return redirect('cart')
        if change_quantity:
            cart.add(change_quantity,quantity, True)
            return redirect('cart')
    return render(request,'cart/cart.html',{'customer':customer,'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

def success(request):
    return render(request,'cart/success.html')

def problem(request):
    return render(request,'cart/problem.html')