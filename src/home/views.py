from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings

from visits.models import PageVisit

LOGIN_URL = settings.LOGIN_URL

def home_view(request, *args, **kwargs):
    PageVisit.objects.create()
    return about_view(request, *args, **kwargs)

def about_view(request):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)

    try:
        percent = (page_qs.count() * 100.0) / qs.count()
    except:
        percent = 0

    PageVisit.objects.create(path=request.path)
    context = {
        'total_visits': qs.count(),
        'page_visits': page_qs.count(),
        'percent': percent
    }

    return render(request, 'home.html', context)

VALID_CODE = '123456'

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    if request.method == 'POST':
        user_pw_sent = request.POST.get('code') or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
    if is_allowed:
        return render(request, 'protected/view.html')
    return render(request, 'protected/entry.html')

@login_required(login_url=LOGIN_URL)
def user_only_view(request, *args, **kwargs):
    return render(request, 'protected/user_only.html')

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, 'protected/staff_only.html')
