from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from subscriptions.models import SubscriptionPrice

# Create your views here.
def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_stripe_id'] = price_id
    return redirect("checkout_start")

@login_required
def checkout_redirect_view(request):
    checkout_subscription_stripe_id = request.session.get("checkout_subscription_stripe_id")
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_stripe_id)
    except:
        obj = None

    if checkout_subscription_stripe_id is None or obj is None:
        return redirect("pricing")
    customer_stripe_id = request.user.customer.stripe_id
    return redirect("/checkout/")

@login_required
def checkout_finalize_view(request):
    return 