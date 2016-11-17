from __future__ import absolute_import, unicode_literals
from celery import shared_task

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

from project_template.settings import MEDIA_ROOT


@shared_task
def create_pdf(account_id):
    from .models import BankAccount
    account = BankAccount.objects.get(id=account_id)
    c = canvas.Canvas('{}/pdfs/{}.pdf'.format(MEDIA_ROOT, account.number))

    text_object = c.beginText()
    text_object.setTextOrigin(cm, 28*cm)
    text_object.setFont("Helvetica-Oblique", 14)

    text_object.textLine('Email: {}'.format(account.user.email))
    text_object.textLine('Account #: {}'.format(account.number))
    text_object.textLine('3D password: {}'.format(account.get_raw_password3d()))
    text_object.textLine('CVV: {}'.format(account.cvv))
    text_object.textLine('Grid:')

    raw_grid = account.get_raw_grid()
    for key in raw_grid:
        text_object.textLine('        {}: {}'.format(key,raw_grid[key]))

    text_object.setFillGray(0.4)

    c.drawText(text_object)
    c.showPage()
    c.save()
