from django.urls import path
from . import views

urlpatterns = [
    path('servers/', views.ServerListApi().as_view()),
    path('servers/<int:pk>/', views.ServerRetrieve().as_view()),
]
