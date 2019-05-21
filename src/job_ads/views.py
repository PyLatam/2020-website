from django.views.generic.list import ListView

from .models import JobAd


class JobAdListView(ListView):
    model = JobAd
    template_name = 'job_ads/list.html'
