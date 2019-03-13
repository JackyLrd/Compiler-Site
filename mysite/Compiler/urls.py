from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'Compiler'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_task', views.create_task, name='create_task'),
    path('create_success',
         auth_views.PasswordChangeDoneView.as_view(template_name='Compiler/create_success.html'),
         name='create_success'),
]
