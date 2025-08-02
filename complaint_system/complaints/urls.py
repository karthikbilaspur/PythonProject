# complaints/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('view/', views.view_complaints, name='view_complaints'),
    path('update/<pk>/', views.update_complaint, name='update_complaint'),
]