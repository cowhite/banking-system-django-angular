from django.shortcuts import render
from rest_framework import generics
from . import models as bankbranch_models
from . import serializers as bankbranch_serializers


class BankBranchListCreateAPIView(generics.ListCreateAPIView):
    queryset = bankbranch_models.BankBranch.objects.all()
    serializer_class = bankbranch_serializers.BankBranchSerializer


class BankBranchRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = bankbranch_models.BankBranch.objects.all()
    serializer_class = bankbranch_serializers.BankBranchSerializer