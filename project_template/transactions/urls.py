from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^initiate/$', views.TransactionView.as_view(), name='initiate_transaction'),
]