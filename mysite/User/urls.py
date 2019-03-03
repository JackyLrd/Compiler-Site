from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'User'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='User/login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='User/index.html', next_page='/'),  name='logout'),
    path('register/', views.register, name = 'register'),
    path('profile/', views.profile, name = 'profile'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='User/change_password.html'), name='change_password'),
    path('change_email/', views.change_email, name = 'change_email'),
]
