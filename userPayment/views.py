from django.shortcuts import render,reverse

from .models import Payment
from .forms import DonationForm
# from .settings import PAYPAL_RECEIVER_EMAIL

# Create your views here.
def payment(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            payment = Payment(
                amount=form.cleaned_data['amount'],
                item_name=form.cleaned_data['item_name'],
                currency_code=form.cleaned_data['currency_code'],
                invoice=form.cleaned_data['invoice'],
                custom=form.cleaned_data['custom']
            )
            payment.save()
            return render(request, 'success.html')
    else:
        paypal_dict = {
            # PayPal form details
            "business": "rehabkosbar@gmail.com",
            "amount": "100.00",
            "currency_code": "USD",
            "item_name": "name of the item",
            "invoice": "unique-invoice-id",
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse('successful')),
            "cancel_return": request.build_absolute_uri(reverse('cancelled')),
        }
        form = DonationForm()

    context = {"form": form}
    return render(request, "payment.html", context)


def payment_successful(request):
    return render(request, 'success.html')


def payment_failed(request):
    return render(request, 'cancel.html')


def paypal_ipn(request):
    # Implement PayPal IPN handling logic here
    pass
