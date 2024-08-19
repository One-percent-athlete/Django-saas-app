from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit

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