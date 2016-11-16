from __future__ import unicode_literals

from django.db import models


# Create your models here.
from django.utils import timezone

from accounts.models import BankAccount

TRANSACTION_STATUS = (
  (0, 'Initiated'),
  (1, 'Declined'),
  (2, 'Aborted'),
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



