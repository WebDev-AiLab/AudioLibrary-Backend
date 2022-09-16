from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.AccountsPrivateView.as_view()),
    path('guest/', views.GuestView.as_view()),
    path('beacon/', views.BeaconView.as_view()),

    # content
    path('tracks/', views.AccountPrivateTracksView.as_view()),

    # simple jwt
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # auth
    path('auth/register/', views.UserRegistrationView.as_view(), name='verify-user'),
    path('auth/verify/', views.UserVerificationView.as_view(), name='verify-user'),
    path('auth/restore/', views.UserRestorePasswordView.as_view(), name='restore-password'),
    path('auth/deactivate/', views.UserDeactivateView.as_view(), name='restore-password'),
    path('auth/create_password/', views.UserChangePasswordView.as_view(), name='restore-password'),
    path('auth/google/', views.UserAuthGoogle.as_view(), name='google-user'),

    # statistics
    path('statistics/', views.StatisticsView.as_view()),

    path('contact/', views.CreateApplicationView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)