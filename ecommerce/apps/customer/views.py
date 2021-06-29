from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, SecurityQuestion
from django.contrib.auth import views as auth_views
from django.contrib import auth
from django.views import View
from .forms import RegisterForm, EditForm, InformationControlForm, PasswordUpdateForm
from .models import User
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from apps.core.decorators import user_password, unauthenticated_user, allowed_users, admin_only, customer_required
from django.contrib import messages


@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('edit_customer')

    else:
        form = RegisterForm()
    return render(request, 'customer/register.html', {'form': form})



@login_required
@customer_required
def customer_profile(request):
    customer = request.user.customer
    orders = customer.orders.all()

    return render(request, 'customer/customer_profile.html', {'customer': customer, 'orders': orders})


def customers(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customers.html', {'customers': customers})


class LogoutView(auth_views.LogoutView):
    template_name = 'customer/customer_profile.html'

    def get_success_url(self):
        return resolve_url('frontpage')


class LoginView(View):
    def get(self, request):
        return render(request, 'customer/customer_login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_customer:  # user.is_active &
                    auth.login(request, user)
                    return redirect('customer_profile')
                messages.error(
                    request, 'Account is not active,please check your email')  
                return render(request, 'customer/customer_login.html')
            messages.error(
                request, 'Invalid credentials,try again')  
            return render(request, 'customer/customer_login.html')

        messages.error(
            request, 'Please fill all fields') 
        return render(request, 'customer/customer_login.html')


@login_required
def edit_customer(request):
    customer = Customer.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = EditForm(data=request.POST,instance=customer)

        if form.is_valid():
            form.save()
            return redirect('customer_profile')

    else:
        form = EditForm(instance=customer)
    return render(request, 'customer/edit_customer.html', {'form': form})


def orders(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = customer.orders.all()
    return render(request, 'customer/orders.html', {'customer': customer, 'orders': orders})


def customer_control(request):
    form = InformationControlForm()
    if request.method == 'POST':
        username = request.POST['username']
        security_question_id = request.POST['security_question']
        security_question_answer = request.POST['security_question_answer']

        security_question = get_object_or_404(SecurityQuestion, pk=security_question_id)

        customer = Customer.objects.get(user__username=username)
        user = User.objects.get(username=username)
        if customer.check_security_question_answer(security_question_answer) & customer.check_security_question(
                security_question):
            if user.is_customer:  
                auth.login(request, user)
                return redirect('password_update')

        else:
            return redirect('frontpage')

    return render(request, 'customer/customer_control.html', {'form': form})

@user_password
def password_update(request):
    #auth.logout(request)
    form = PasswordUpdateForm()
    if request.method == 'POST':

        username = request.POST['username']
        user = User.objects.get(username=username)
        password = request.POST['password1']
        user.set_password(password)
        user.save()
        return redirect('password_success')

    else:
        form = PasswordUpdateForm()
    return render(request, 'customer/password_update.html', {'form': form})


def password_success(request):
    return render(request, 'customer/customer_password_success.html')
