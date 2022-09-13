from django.urls import path, include
from .views import PageView

urlpatterns = [
    path('pages/', PageView.as_view({'get': 'list'})),
    path('page/', PageView.as_view({'get': 'retrieve'})),
]