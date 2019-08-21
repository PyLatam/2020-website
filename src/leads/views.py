from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from account.models import Account

from .models import LeadGroup


@login_required
def register_lead(request, username):
    group = LeadGroup.get_for_user(request.user)

    if group:
        account = get_object_or_404(
            Account,
            user__username=username,
            registration__isnull=False,
        )
        group.leads.add(account)
        return HttpResponse(status=201)
    raise PermissionDenied
