from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
from paypal.standard.forms import PayPalPaymentsForm
from estore.utils import get_code, add_item, remove_item
from estore.models import Cart, Item

def index(request):
    template = loader.get_template('estore/index.html')
    code = get_code(request)
    cart_items = Cart.objects.filter(code=code)[0].items.all()
    items = Item.objects.all()
    context = {'items' : items, 'cart' : cart_items}

    response = HttpResponse(template.render(context, request))
    response.set_cookie('cart', code)
    return response

def add(request):
    item_id = request.GET.get('item', '')[4:]
    code = get_code(request)
    success = add_item(code, item_id)
    if (not success):
        return HttpResponse("Add")

    response = HttpResponse("Remove")
    response.set_cookie('cart', code)
    return response

def remove(request):
    item_id = request.GET.get('item', '')[4:]
    code = get_code(request)
    success = remove_item(code, item_id)
    if (not success):
        return HttpResponse("Remove")

    response = HttpResponse("Add")
    response.set_cookie('cart', code)    
    return response

@login_required
def account_profile(request):
    return HttpResponse("Hi, {0}! Nice to meet you.".format(request.user))


def account_logout(request):
    """
    Logout and redirect to the main page.
    """
    logout(request)
    return redirect('/')

@csrf_exempt
def paypal_success(request):
    """
    Tell user we got the payment.
    """
    return HttpResponse("Money is mine. Thanks.")


@login_required
def paypal_pay(request):
    template = loader.get_template('estore/cart.html')
    code = get_code(request)
    cart_items = Cart.objects.filter(code=code)[0].items.all()
    price = 0
    for item in cart_items:
        price += item.price


    template = loader.get_template('estore/cart.html')
    paypal_dict = {
        "business": "mnovikova@gmail.com",
        "amount": str(price) + ".00",
        "currency_code": "RUB",
        "item_name": "some products",
        "invoice": code,
        "notify_url": reverse('paypal-ipn'),
        "return_url": "http://localhost:8000/payment/success/",
        "cancel_return": "http://localhost:8000/payment/cart/",
        "custom": str(request.user.id)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "paypal_dict": paypal_dict, "cart": cart_items, "price": price}

    response = HttpResponse(template.render(context, request))
    response.set_cookie('cart', code)
    return response
    
