from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date

class Region(models.Model):
    name = models.CharField(max_length=30)
    description=models.CharField(max_length=30)
    def __str__(self):
        return self.name
# --------------------------
# Patient
# --------------------------
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+','A+'),('A-','A-'),
        ('B+','B+'),('B-','B-'),
        ('AB+','AB+'),('AB-','AB-'),
        ('O+','O+'),('O-','O-')
    ]
    # Core identity
    card_number = models.CharField(max_length=15, unique=True, editable=False, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)

    # Contact & Location
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    town = models.CharField(max_length=40, null=True, blank=True)
    woreda = models.CharField(max_length=40, null=True, blank=True)
    kebele = models.CharField(max_length=40, null=True, blank=True)
    house_number = models.CharField(max_length=40, null=True, blank=True)

    # Registration info
    registered_date = models.DateTimeField(default=timezone.now)
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_registered'
    )
    is_active = models.BooleanField(default=False)
    activated_date = models.DateTimeField(default=timezone.now)

    # MRN Generation (Improved with UUID fallback)
    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = self.generate_unique_card_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_card_number():
        last_patient = Patient.objects.order_by('-id').first()
        if last_patient and last_patient.card_number:
            try:
                last_number = int(last_patient.card_number.split('-')[-1])
                new_number = last_number + 1
            except ValueError:
                new_number = 1
        else:
            new_number = 1
        return f"{new_number:05d}"

    @property
    def age(self):
        """Calculate age dynamically from date_of_birth"""
        today = date.today()
        if self.date_of_birth:
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def __str__(self):
        return f"{self.full_name}/MRN:{self.card_number}"


