from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .apps import UsersConfig
from .views import RegisterView, ProfileView, email_verification, ResetView, PasswordResetDone, ResetConfirmView, \
    ResetCompleteView, UserListView, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user_form/', ProfileView.as_view(), name='user_form'),
    path('users/password_reset/', ResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetConfirmView.as_view(), name='password_confirm'),
    path('users/reset/compete/', ResetCompleteView.as_view(), name='complete'),
    path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:pk>/delete', UserDeleteView.as_view(), name='user_confirm_delete'),
]
