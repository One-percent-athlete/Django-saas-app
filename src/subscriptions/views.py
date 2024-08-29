from django.shortcuts import render

from subscriptions.models import SubscriptionPrice

def subscription_price_view(request):
    qs = SubscriptionPrice.objects.filter(featured=True)
    monthly_qs = SubscriptionPrice.objects.filter(interval=SubscriptionPrice.IntervalChoices.MONTHLY)
    yearly_qs = SubscriptionPrice.objects.filter(interval=SubscriptionPrice.IntervalChoices.MONTHLY)
    return render(request, "subscription/pricing.html", {
        "monthly_qs": monthly_qs,
        "yearly_qs": yearly_qs,
    })