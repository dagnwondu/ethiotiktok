from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = "admin", "Admin"
        DOCTOR = "doctor", "Doctor"
        NURSE = "nurse", "Nurse"
        RECEPTIONIST = "receptionist", "Receptionist"
        PHARMACIST = "pharmacist", "Pharmacist"
        LAB_TECHNICIAN = "lab_technician", "Lab Technician"
        CASHIER = "cashier", "Cashier"
        FINANCE = "finance", "Finance"
        ACCOUNTANT = "accountant", "Accountant"
        PATIENT = "patient", "Patient"
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.PATIENT
    )
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.username}"
    class Meta:
        permissions = [
            ("can_register_patients", "Can register patients"),
            ("can_view_patients", "Can view patient records"),
            ("can_edit_patients", "Can edit patient records"),
            ("can_delete_patients", "Can delete patient records"),
            ("can_schedule_appointments", "Can schedule appointments"),
            ("can_view_appointments", "Can view appointments"),
            ("can_edit_appointments", "Can edit appointments"),
            ("can_delete_appointments", "Can delete appointments"),
            ("can_manage_inventory", "Can manage inventory"),
            ("can_view_reports", "Can view reports"),
            ("can_generate_reports", "Can generate reports"),
            ("can_manage_users", "Can manage user accounts"),
            ("can_view_billing", "Can view billing information"),
            ("can_edit_billing", "Can edit billing information"),
            ("can_process_payments", "Can process payments"),
        ]