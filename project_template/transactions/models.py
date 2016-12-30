from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import string
import random

# Create your models here.
from django.db.models import signals
from django.utils import timezone

from accounts.models import BankAccount
from project_template.settings import SMS_OTP_VALIDITY_MINS
from .tasks import *


TRANSACTION_STATUS = (
  (0, 'Initiated'),
  (1, 'Declined'),
  (2, 'Aborted'),
  (3, 'Successful'),
)


TRANSFER_PROCESS_STATUS = (
  (0, 'Initiated'),
  (1, 'Timed out'),
  (2, 'Successful'),
  (3, 'Invalid')
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

  def get_transfer_process(self):
    try:
      return TransferProcess.objects.get(transaction=self)
    except models.Model.DoesNotExist:
      return None

  def initiate_transfer(self):
    transfer_process = TransferProcess(transaction=self)
    transfer_process.save()
    return transfer_process

  def decline(self):
    self.status = 1
    self.save()
    return self

  def abort(self):
    self.status = 2
    self.save()
    return self

  def transfer(self):
    if self.status == 2:
      raise Exception('This Transaction is aborted')

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
    return self


class TransferProcess(models.Model):
  transaction = models.ForeignKey(Transaction)
  otp = models.CharField(max_length=128)
  grid_code = models.CharField(max_length=3)
  status = models.IntegerField(choices=TRANSFER_PROCESS_STATUS, default=0)
  valid_till = models.DateTimeField()

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
    self.send_otp(self._raw_otp)
    self.set_otp(self._raw_otp)

    # grid code generation
    self.grid_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))

    # update validity
    self.valid_till = timezone.now() + timezone.timedelta(minutes=SMS_OTP_VALIDITY_MINS)

    # validate from account
    if BankAccount.objects.filter(number=self.transaction.from_account_number).count() == 0:
      self.status = 3

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

  def authenticate_transfer(self, raw_otp, raw_grid_code):
    if timezone.now() > self.valid_till:
      self.status = 1

    if self.check_otp(raw_otp) and self.check_grid_code(raw_grid_code) and self.status == 0:
      self.status = 2
      self.transaction.transfer()

    self.save()
    return self

  def get_raw_otp(self):
    if self._raw_otp:
      return self._raw_otp
    else:
      return None

  def send_otp(self, otp):
    self._from_account_number = self.transaction.from_account_number
    self._mobile_num = BankAccount.objects.get(number=self._from_account_number)
    mobile_num = self._mobile_num.mobile_num.as_e164
    send_twilio_message(mobile_num, otp)


def initiate_transfer_process_on_transaction_creation(sender, instance, created, **kwargs):
  if created:
    instance.initiate_transfer()

signals.post_save.connect(initiate_transfer_process_on_transaction_creation, sender=Transaction)
