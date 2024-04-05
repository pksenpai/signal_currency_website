from django.urls import path
from .views import AddSignalView


app_name = 'posts'
urlpatterns = [
    path('add/', AddSignalView.as_view(), name="add"),
]
