from django.urls import path
from .views import PasswordsChangeView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('search', views.search, name='search'),
    path('student', views.student, name='student'),
    path('new_student', views.new_student, name='new_student'),
    path('password', PasswordsChangeView.as_view(template_name='secretaria/change-password.html'), name='password'),
    path('listados', views.listados, name='listados'),
    path('listados_process', views.listados_process, name='listados_process'),
    path('salida/<int:student_pk>', views.salida, name='salida')
]

