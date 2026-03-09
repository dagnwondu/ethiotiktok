from django.shortcuts import render
from . forms import PatientForm
from authentication.views import role_required
from billing.models import Invoice, InvoiceItem, Service
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# from visits.models import Visit

# @permission_required('authentication.can_register_patients', raise_exception=True)


# Create your views here.
@role_required(['receptionist'])
def register_patient(request):
    if request.method == "POST":
        # 1. Create Patient object
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.is_active = True  # Ensure the patient is active
            patient.registered_by=request.user
            patient.save()
            # 2. Create visit (initial visit)
            # visit = Visit.objects.create(
            #     patient=patient,
            #     assigned_by=request.user,
            #     status="waiting"
            # )


            # 4. Add registration fee service
            try:
                registration_service = Service.objects.get(name="Registration")
                # 3. Create invoice
                invoice = Invoice.objects.create(
                    patient=patient,
                    generated_by = request.user,
                )
                
                invoice_item = InvoiceItem.objects.create(
                    invoice=invoice,
                    service = Service.objects.get(name='Registration'),
                    unit_price=Service.objects.get(name='Registration').unit_price ,               
                    quantity=1

                )
            except Service.DoesNotExist:
                messages.error(
                    request,
                    "Registration service not configured. Contact admin."
                )
                        
                return redirect("receptionist_dashboard")

            messages.success(
                request,
                "Patient registered successfully. Please proceed to payment."
            )

            # 5. Redirect cashier (or invoice detail)
            return redirect("receptionist_dashboard")

    else:
        form = PatientForm()

    return render(request, "patient/register_patient.html", {"form": form})

# views.py
from django.shortcuts import render
from patient.models import Patient
from billing.models import Invoice

# Active OPD patients
def active_opd_patients(request):
    patients = Patient.objects.filter(
        episodes__episode_type='outpatient',
        episodes__status='active'
    ).distinct()
    return render(request, "patient/patient_list.html", {"patients": patients, "title": "Active OPD Patients"})

# Active IPD patients
def active_ipd_patients(request):
    patients = Patient.objects.filter(
        episodes__episode_type='inpatient',
        episodes__status='active'
    ).distinct()
    return render(request, "patient/patient_list.html", {"patients": patients, "title": "Admitted IPD Patients"})

# Waiting for registration payment (no episode yet)
def waiting_registration_patients(request):
    patients = Patient.objects.filter(
        episodes__isnull=True,
        invoices__status__in=['draft','issued','partial']
    ).distinct()
    return render(request, "patient/patient_list.html", {"patients": patients, "title": "Waiting Registration Payment"})

# ER / Emergency patients
def active_er_patients(request):
    patients = Patient.objects.filter(
        episodes__episode_type='emergency',
        episodes__status='active'
    ).distinct()
    return render(request, "patient/patient_list.html", {"patients": patients, "title": "ER / Emergency Patients"})

# Walk-in patients (example: patients with type 'walkin')
def walkin_patients(request):
    patients = Patient.objects.filter(
        episodes__episode_type='walkin',
        episodes__status='active'
    ).distinct()
    return render(request, "patient/patient_list.html", {"patients": patients, "title": "Walk-in Patients"})

# Assigned patients (already assigned to doctor or nurse)
def assigned_patients(request):
    patients = Patient.objects.filter(
        episodes__isnull=False,
        episodes__status='active'
    ).distinct()
    return render(request, "patient/patient_list.html", {"patients": patients, "title": "Assigned Patients"})