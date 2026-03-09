from django import forms
from .models import Patient, Region

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'full_name', 'phone_number', 'gender', 'blood_group', 'region',
            'region', 'town', 'woreda', 'kebele', 'house_number', 'date_of_birth'
        ]
        widgets = {
            'gender': forms.Select(choices=Patient.GENDER_CHOICES),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default region for new patients
        if not self.instance.pk:
            self.fields['region'].initial = Region.objects.first()

    # Optional: clean phone_number
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

# For quick updates (e.g., contact info)
class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone_number', 'town', 'woreda', 'kebele', 'house_number']
