from django.urls import path

from . import views

app_name = "assignments"

urlpatterns = [

path('', views.assignment_list, name='list'),
path('create/', views.create_assignment, name='create'),
path("submit/<int:pk>/", views.submit_assignment, name="submit"),
path('grading/<int:pk>/', views.grading, name='grading'),
path('feedback/<int:pk>/', views.feedback, name='feedback'),
path('submissions/', views.submissions, name='submissions'),
path("<int:pk>/", views.assignment_detail, name="detail"),
path("publish/<int:pk>/", views.publish_assignment, name="publish"),
path("<int:pk>/", views.assignment_detail, name="detail")
]