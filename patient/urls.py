
from django.urls import path
from . import views

urlpatterns = [
    path('register_patient/', views.register_patient, name = 'register_patient'),
    # path('patients/opd/', views.active_opd_patients, name='active_opd_patients'),
    # path('patients/ipd/', views.active_ipd_patients, name='active_ipd_patients'),
    # path('patients/waiting-payment/', views.waiting_registration_patients, name='waiting_registration_patients'),
    # path('patients/er/', views.active_er_patients, name='active_er_patients'),
    # path('patients/walkin/', views.walkin_patients, name='walkin_patients'),
    # path('patients/assigned/', views.assigned_patients, name='assigned_patients'),
    ]