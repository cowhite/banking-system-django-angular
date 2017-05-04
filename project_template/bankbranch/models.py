from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class BankBranch(models.Model):
    code = models.CharField(max_length=16)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    pincode = models.CharField(max_length=6)
    district = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    ifsc_code = models.CharField(max_length=16)
    # TODO: add manager once users created
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
