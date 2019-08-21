import io

import qrcode

from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import LeadCode


def get_user_qr_code(user):
    domain = Site.objects.get_current().domain
    lead_url = domain + reverse('register_lead', args=[user.username])
    lead_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    lead_code.add_data(lead_url)
    lead_code.make(fit=True)
    return lead_code.make_image(fill_color="black", back_color="white")


def set_user_qr_code(user):
    buffer = io.BytesIO()
    qr_code = get_user_qr_code(user)
    qr_code.save(buffer, format='PNG')
    lead = LeadCode.objects.get_or_create(account=user.account)[0]
    lead.code_image = SimpleUploadedFile(name='qrcode.png', content=buffer.getvalue())
    lead.save(update_fields=('code_image',))
    return lead
