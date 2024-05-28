from django.urls import path, re_path
from .views import AddSignalView, DetailSignalView


app_name = 'posts'
urlpatterns = [
    path('add/', AddSignalView.as_view(), name="add"),
    re_path(r'^(?P<slug>[-\w]*)/$', DetailSignalView.as_view(), name="details"),
]
