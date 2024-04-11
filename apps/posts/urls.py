from django.urls import path
from .views import AddSignalView, DetailSignalView


app_name = 'posts'
urlpatterns = [
    path('add/', AddSignalView.as_view(), name="add"),
    path('details/<slug:slug>', DetailSignalView.as_view(), name="details"),
]
