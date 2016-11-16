from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models


from django.db.models import Max

import string
import random

from django.contrib.auth.models import User
from django.db.models import signals

# Create your models here.


class BankAccount(models.Model):
  user = models.ForeignKey(User)
  number = models.CharField(max_length=12, unique=True)
  password3d = models.CharField(max_length=128)
  grid = JSONField()
  cvv = models.CharField(max_length=3)

  def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
    if self.pk is None:
      #Account Number generation
      prev_acc_num = BankAccount.objects.aggregate(max=Max('number'))['max']
      if prev_acc_num == '':
        prev_acc_num = 0
      self.number = str(int(prev_acc_num) + 1).zfill(12)

      #3dpassword generation
      self._raw_password3d = ''.join(random.choice(string.digits) for _ in range(6))
      self.set_password3d(self._raw_password3d)

      #CVV Generation
      self.cvv = ''.join(random.choice(string.digits) for _ in range(3))

      #grid generation
      key = 'A'
      self._raw_grid = {}
      self.grid = {}

      for i in range(16):
        rnd = ''.join(random.choice(string.digits) for _ in range(2))
        self._raw_grid[key] = rnd
        self.grid[key] = make_password(rnd)
        key = chr(ord(key) + 1)

    return super(BankAccount, self).save(
      force_insert=force_insert,
      force_update=force_update,
      using=using,
      update_fields=update_fields
    )

  def set_password3d(self, raw_password):
    self.password3d = make_password(raw_password)

  def check_password3d(self, raw_password):

    def setter(raw_password):
      self.set_password3d(raw_password)

      self._raw_password3d = None
      self.save(update_fields=["password"])

    return check_password(raw_password, self.password, setter)


def create_bank_account(sender, instance, created, **kwargs):
    if created:
      acc = BankAccount(user=instance)
      acc.save()

signals.post_save.connect(create_bank_account, sender=User)