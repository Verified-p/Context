from django.urls import path
from . import views

app_name = "lessons"

urlpatterns = [

    path('', views.lesson_list, name='lesson_list'),
    path('<int:pk>/', views.lesson_detail, name='lesson_detail'),

    path('create/', views.create_lesson, name='create_lesson'),
    path('<int:pk>/edit/', views.edit_lesson, name='edit_lesson'),

    path('progress/', views.lesson_progress, name='lesson_progress'),
]