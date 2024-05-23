from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout'),  # Use the custom logout view
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(extra_context={'next_page': '/home'}), name='password_reset_complete'),
    path('profile/',views.user_profile, name='profile'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete-account/', views.delete_account, name='delete_account'),
   
    
]
