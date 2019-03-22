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
    path('check_task', views.check_task, name='check_task'),
    path('modify_success',
         auth_views.PasswordChangeDoneView.as_view(template_name='Compiler/modify_success.html'),
         name='modify_success'),
    path('start_compile', views.start_compile, name='start_compile'),
    path('stop_compile', views.stop_compile, name='stop_compile'),
    path('get_target', views.get_target, name='get_target'),
]
