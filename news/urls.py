from django.urls import path

from news.views import PostView

urlpatterns = [
    path('posts/', PostView.as_view({'get': 'list'})),
    path('posts/<str:slug>/', PostView.as_view({'get': 'retrieve'})),
]