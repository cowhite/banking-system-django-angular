from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics


# Create your views here.
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionView(generics.ListCreateAPIView):
  serializer_class = TransactionSerializer
  queryset = Transaction.objects.all()