from rest_framework import serializers
from . import models as bankbranch_models


class BankBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = bankbranch_models.BankBranch
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')