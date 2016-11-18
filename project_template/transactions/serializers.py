from rest_framework import serializers

from transactions.models import TransferProcess, Transaction, TRANSACTION_STATUS

TRANSACTION_STATUS = {n[0]: n[1] for n in TRANSACTION_STATUS}


class TransactionSerializer(serializers.ModelSerializer):
  status = serializers.SerializerMethodField()

  class Meta:
    model = Transaction
    fields = '__all__'
    read_only_fields = (
      'created_at,'
      'updated_at',
    )

  def get_status(self,obj):
    return TRANSACTION_STATUS[obj.status]


class TransferProcessSerializer(serializers.ModelSerializer):
  class Meta:
    model = TransferProcess
    fields = '__all__'
    depth = 1
    read_only_fields = (
      'created_at,'
      'updated_at',
    )

