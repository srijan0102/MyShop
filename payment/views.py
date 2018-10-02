from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
import braintree


@csrf_exempt  # avoid csrf expectations
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    if request.method == 'POST':
        # Retrieve once
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transactions
        results = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if results.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = results.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', context={'order': order, 'client_token': client_token})
    # paypal_dict = {
    #     'business': settings.PAYPAL_RECEIVER_EMAIL,
    #     'amount': '%2f' % order.get_total_cost().quantize(Decimal('.01')),
    #     'item_name': 'Order{}'.format(order.id),
    #     'invoice': str(order.id),
    #     'currency_code': 'USD',
    #     'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
    #     'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
    #     'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    # }
    # form = PayPalPaymentsForm(initial=paypal_dict)
    # return render(request, 'payment/process.html', {'order': order, 'form': form})
