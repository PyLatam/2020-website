from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Talk, TimeSlot


def landing(request):
    dates = TimeSlot.objects.dates('start__date', 'day')
    schedule = [
        (date, TimeSlot.objects.filter(start__date=date)) for date in dates
    ]
    return render(request, 'schedule/landing.html', {'schedule': schedule})


class TalkDetail(DetailView):
    queryset = Talk.objects.filter(time_slot__isnull=False)
    template_name = 'schedule/detail.html'
