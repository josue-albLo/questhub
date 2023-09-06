from django.urls import path

from . import views

app_name = 'quest'

urlpatterns = [
    path('', views.index, name='index'),
    path("main/", views.mian_page, name='main'),
    path('answer/', views.answer, name='answer'),
]