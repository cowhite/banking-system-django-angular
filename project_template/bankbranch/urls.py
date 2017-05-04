from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.BankBranchListCreateAPIView.as_view(), name="branches_list_create"),
    url(r'^(?P<pk>\d+)/$', views.BankBranchListCreateAPIView.as_view(), name="branches_list_create"),
]