from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.page_profile, name='profile'),
    path('<int:user_id>/', views.userid_profile, name='userid_profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logged_out.html'), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),#How to Add Social Login to Django
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='auth/password_change_form.html'),  name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]