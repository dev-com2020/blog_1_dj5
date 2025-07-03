from django.urls import path

from quiz_project.quiz_app import views

urlpatterns = [
    path('', views.home, name='home'),
]