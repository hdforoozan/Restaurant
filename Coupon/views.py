from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponForm
from django.contrib import messages

@require_POST
def coupon_apply(request):

    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now , valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
            print("coupon_id added to session")
        except Coupon.DoesNotExist:
            messages.error(request,'The time for this coupon is passed.')
            request.session['coupon_id'] = None

    return redirect('cart_detail')
