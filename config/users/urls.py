from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .apps import UsersConfig
from .views import RegisterView, email_verification, ResetView, PasswordResetDone, ResetConfirmView, \
    ResetCompleteView, UserListView, UserDeleteView, profile
from . import views

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/password_reset/', ResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetConfirmView.as_view(), name='password_confirm'),
    path('users/reset/compete/', ResetCompleteView.as_view(), name='complete'),
    path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:pk>/delete', UserDeleteView.as_view(), name='user_confirm_delete'),
    path('profile/', profile, name='profile'),
    path('community/', views.community, name='community'),
    path('posts/create/', views.create_post, name='create_post'),  # Добавьте эту строку
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('groups/<int:group_id>/join/', views.join_group, name='join_group'),
]
