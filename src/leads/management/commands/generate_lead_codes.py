from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from leads.helpers import set_user_qr_code


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.filter(account__registration__isnull=False)

        for user in users.select_related('account'):
            set_user_qr_code(user)
