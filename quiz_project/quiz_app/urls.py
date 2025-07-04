from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/',TestListView.as_view(), name='history'),
    path('download/<int:test_id>', download, name='test_download'),
]