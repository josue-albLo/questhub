from django.urls import path

from . import views

app_name = 'quest'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path("main/", views.mian_page, name='main'),
    path('createquestion/<int:pk>', views.create_question, name='createquestion'),
    path('processingquestion/<int:pk>', views.procesing_question, name='processingquestion'),
    path('answer/<int:id_question>/<int:pk_user>', views.answer, name='answer'),
    path('createanswer/<int:pk_question>/<int:pk_user>', views.create_answer, name='createanswer'),
    path('save_answer/<int:pk_question>/<int:pk_user>', views.save_answer, name='saveanswer'),
    path('votequestion/<int:pk_question>/<int:pk_user>', views.vote_question, name='votequestion'),
]