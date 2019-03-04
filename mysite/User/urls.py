from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy

from . import views

app_name = 'User'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='User/index.html', next_page=reverse_lazy('index')),
         name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='User/change_password.html',
                                                                   success_url=reverse_lazy(
                                                                       'User:password_change_done')),
         name='change_password'),
    path('password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='User/password_change_done.html'),
         name='password_change_done'),
    path('change_profile/', views.change_profile, name='change_profile'),

]
