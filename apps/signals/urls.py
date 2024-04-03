from django.urls import path
from .views import AddSignalView


app_name = 'signals'
urlpatterns = [
    path('add/', AddSignalView.as_view(), name="add"),
]
