from django.urls import path, include
from .views import LoginView, LogoutView, SignupView, VerifyTokenView, UpdatePasswordView

urlpatterns = [
    path('login',LoginView.as_view(), name = 'login'),
    path('logout',LogoutView.as_view(), name='auth_logout'),
    path('signup',SignupView.as_view(), name='auth_signup'),
    path('verify',VerifyTokenView.as_view(), name='token_verify'),
    path('update_password',UpdatePasswordView.as_view(), name='update_password'),
    # path('reset',include('django_rest_passwordreset.urls', namespace='password_reset')),
]
