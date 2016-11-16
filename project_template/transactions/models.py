from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import string
import random

# Create your models here.
from django.utils import timezone

from accounts.models import BankAccount

TRANSACTION_STATUS = (
  (0, 'Initiated'),
  (1, 'Declined'),
  (2, 'Aborted'),
  (3, 'Successful'),
)


TRANSFER_PROCESS_STATUS = (
  (0, 'Initiated'),
  (1, 'Request Sent'),
  (2, 'Timed out'),
  (3, 'Successful'),
)


class Transaction(models.Model):
  from_account_number = models.CharField(max_length=12)
  to_account_number = models.CharField(max_length=12)
  amount = models.DecimalField(max_digits=20, decimal_places=2)
  status = models.IntegerField(choices=TRANSACTION_STATUS, default=0)

  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def save(self, force_insert=False, force_update=False, using=None,
           update_fields=None):

    # Update timestamp
    self.updated_at = timezone.now()

    return super(Transaction, self).save(
      force_insert=force_insert,
      force_update=force_update,
      using=using,
      update_fields=update_fields
    )

  def abort(self):
    self.status = 1
    self.save()
    return self

  def transfer(self):
    try:
      from_acc = BankAccount.objects.get(number=self.from_account_number)
    except models.Model.DoesNotExist:
      from_acc = None

    try:
      to_acc = BankAccount.objects.get(number=self.to_account_number)
    except models.Model.DoesNotExist:
      to_acc = None

    if from_acc:
      if from_acc.balance < self.amount:
        raise Exception('Insufficient Funds')
      from_acc.balance = from_acc.balance - self.amount
      from_acc.save()

    if to_acc:
      to_acc.balance = to_acc.balance + self.amount
      to_acc.save()

    self.status = 3
    self.save()
    return self


class TransferProcess(models.Model):
  transaction = models.ForeignKey(Transaction)
  otp = models.CharField(max_length=128)
  grid_code = models.CharField(max_length=3)

  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def save(self, force_insert=False, force_update=False, using=None,
           update_fields=None):
    if self.pk is None:
      self.initialize_transfer_process()

    # Update timestamp
    self.updated_at = timezone.now()

    return super(TransferProcess, self).save(
      force_insert=force_insert,
      force_update=force_update,
      using=using,
      update_fields=update_fields
    )

  def initialize_transfer_process(self):
    # otp generation
    self._raw_otp = ''.join(random.choice(string.digits) for _ in range(6))
    self.set_otp(self._raw_otp)

    # grid code generation
    self.grid_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))

  def set_otp(self, raw_otp):
    self.otp = make_password(raw_otp)

  def check_otp(self, raw_otp):

    def setter(raw_password):
      self.set_otp(raw_password)

      self._raw_otp = None
      self.save(update_fields=["otp"])

    return check_password(raw_otp, self.otp, setter)

  def check_grid_code(self, raw_grid_code):
    from_acc = BankAccount.objects.get(number=self.transaction.from_account_number)

    if len(raw_grid_code) == 6:

      for char in self.grid_code:

        if not from_acc.check_grid_single(raw_grid_code[:2], char):
          return False

        raw_grid_code = raw_grid_code[2:]

      return True

    else:
      return False

