from estore.models import *
import uuid 

def get_code(request):
    c = request.COOKIES.get('cart')
    if ((c == None) or (len(Cart.objects.filter(code=c)) == 0)):
        c = uuid.uuid4().hex[:20].upper()
        cart = Cart(code=c)
        cart.save()
    return c

def add_item(code, item_id):
    cart = Cart.objects.filter(code=code)[0]

    items = Item.objects.filter(id=item_id)
    if (len(items) == 0):
        return False
    item = items[0]
    if (item not in cart.items.all()):
        cart.items.add(item)
        cart.save()
    return True

def remove_item(code, item_id):
    cart = Cart.objects.filter(code=code)[0]

    items = Item.objects.filter(id=item_id)
    if (len(items) == 0):
        return False
    item = items[0]
    cart.items.remove(item)
    cart.save()
    return True