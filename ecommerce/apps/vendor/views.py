from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor
from django.utils.text import slugify
from apps.product.models import Product
from .forms import ProductForm
from .forms import RegisterForm
from .models import User
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url
from apps.core.decorators import unauthenticated_user,allowed_users,vendor_required
from django.contrib import messages
from django.contrib import auth
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import mimetypes
import os
from django.conf import settings

@unauthenticated_user
def become_vendor(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)

            vendor=Vendor.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')

    else:
        form =RegisterForm()
    return render(request,'vendor/become_vendor.html', {'form':form})


@login_required
@vendor_required
def vendor_admin(request):
    vendor = request.user.vendor
    products =vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount=0
        order.vendor_paid_amount=0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor==request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()

                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False


    return render(request,'vendor/vendor_admin.html',{'vendor':vendor,'products':products, 'orders':orders})

@login_required
def add_product(request):
    if request.method =='POST':
        form =ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor=request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html',{'form':form})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name','')
        email=request.POST.get('email','')

        if vendor.name==name:
            vendor.created_by.email=email
            vendor.created_by.save()
            vendor.save()

            return redirect('vendor_admin')

    return render(request, 'vendor/edit_vendor.html',{'vendor':vendor})




def vendors(request):
    vendors= Vendor.objects.all()
    return render(request, 'vendor/vendors.html',{'vendors':vendors})

def vendor(request, vendor_id):
    vendor=get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendor/vendor.html',{'vendor':vendor})





class LogoutView(auth_views.LogoutView):
    template_name = 'vendor/vendor_admin.html'
    def get_success_url(self):
        return resolve_url('frontpage')



class LoginView(View):
    def get(self, request):
        return render(request, 'vendor/vendor_login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_vendor:
                    auth.login(request, user)

                    return redirect('vendor_admin')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'vendor/vendor_login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'vendor/vendor_login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'vendor/vendor_login.html')



def html_to_pdf_view(request):
    vendor = request.user.vendor
    products =vendor.products.all()
    orders = vendor.orders.all()
    for order in orders:
        order.vendor_amount=0
        order.vendor_paid_amount=0
        order.fully_paid = True

        for item in order.items.all():

            if item.vendor==request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()

                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    html_string = render_to_string('vendor/pdf_template.html',{'vendor':vendor,'products':products, 'orders':orders})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/orders.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('orders.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
        return response

    return response

