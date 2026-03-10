
from django.urls import path
from . import views
from .views import CustomLoginView, MyUsersView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('receptionist_dashboard/', views.receptionist_dashboard, name = 'receptionist_dashboard'),
    path('streamer_dashboard/', views.streamer_dashboard, name = 'streamer_dashboard'),   
    path('finance_dashboard/', views.finance_dashboard, name = 'finance_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name = 'doctor_dashboard'),
    path('users_management/', MyUsersView.as_view(), name= 'users_management'),    
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('password_change/', views.password_change, name='password_change'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),
    path('logout/', views.logout, name = 'logout'),
    ]


