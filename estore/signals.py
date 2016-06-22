from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.core.mail import send_mail

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        code = ipn_obj.invoice
        try:
            items = Cart.objects.filter(code=code)[0].items.all()
            for item in items:
                item.amount = max(0, item.amount - 1)
        except:
            pass
        if ipn_obj.receiver_email != "aesamburov-facilitator@gmail.com":
            return


        #send_mail(
        #    '1',
        #    '2',
        #    'aesamburov-facilitator@gmail.com',
        #    ['aesamburov@gmail.com'],
        #    fail_silently=False,
        #)
    else:
        pass

print('????????????????????????????')
valid_ipn_received.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money)
print('????????????????????????????')