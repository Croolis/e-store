from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
from paypal.standard.forms import PayPalPaymentsForm
from estore.utils import get_code, get_cost, add_item, remove_item
from estore.models import Cart, Item, Category

def index(request, category_id = -1):
    import estore.signals
    template = loader.get_template('estore/index.html')
    code = get_code(request)
    cart_items = Cart.objects.filter(code=code)[0].items.all()
    selected = 0
    if category_id == -1:
        items = Item.objects.all()
    else:
        category = Category.objects.filter(id=category_id)  
        try:
            items = Item.objects.filter(category=category[0])
            selected = category[0].id
        except:
            items = Item.objects.all()
    context = {'items' : items, 'cart' : cart_items, 
    'categories' : Category.objects.all(), 'selected' : selected}

    response = HttpResponse(template.render(context, request))
    response.set_cookie('cart', code)
    return response

def item(request, item_id = 1):
    template = loader.get_template('estore/item.html')
    item = Item.objects.filter(id=item_id)[0]
    context = {'item' : item}

    response = HttpResponse(template.render(context, request))
    return response

def add(request):
    item_id = request.GET.get('item', '')[4:]
    code = get_code(request)
    success = add_item(code, item_id)
    if (not success):
        return HttpResponse('{"text":"Add", "cost":-1}')

    cost = get_cost(get_code(request))
    response = HttpResponse('{"text":"Remove", "cost":'+str(cost)+'}')
    response.set_cookie('cart', code)
    return response

def remove(request):
    item_id = request.GET.get('item', '')[4:]
    code = get_code(request)
    success = remove_item(code, item_id)
    response = HttpResponse()
    if (not success):
        return HttpResponse('{"text":"Remove", "cost":-1}')

    cost = get_cost(get_code(request))
    response = HttpResponse('{"text":"Add", "cost":'+str(cost)+'}')
    response.set_cookie('cart', code)
    return response

def cart(request):
    template = loader.get_template('estore/cart.html')
    code = get_code(request)
    cart_items = Cart.objects.filter(code=code)[0].items.all()
    price = 0
    for item in cart_items:
        price += item.price

    context = {"cart": cart_items, "price": price}

    response = HttpResponse(template.render(context, request))
    response.set_cookie('cart', code)
    return response    

@login_required
def account_profile(request):    
    template = loader.get_template('estore/profile.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response


def account_logout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def paypal_success(request):
    template = loader.get_template('estore/success.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    response.delete_cookie('cart')
    return response


@login_required
def paypal_pay(request):
    template = loader.get_template('estore/payment.html')
    code = get_code(request)
    cart_items = Cart.objects.filter(code=code)[0].items.all()
    price = 0
    for item in cart_items:
        price += item.price
    paypal_dict = {
        "business": "aesamburov-facilitator@gmail.com",
        "amount": str(price) + ".00",
        "currency_code": "RUB",
        "item_name": "some products",
        "invoice": code,
        "notify_url": "http://127.0.0.1:8000" + reverse('paypal-ipn'),
        "return_url": "http://127.0.0.1:8000/payment/success/",
        "cancel_return": "http://127.0.0.1:8000/payment/cart/",
        "custom": str(request.user.id)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "paypal_dict": paypal_dict}
    response = HttpResponse(template.render(context, request))
    response.delete_cookie('cart')
    return HttpResponse(template.render(context, request))