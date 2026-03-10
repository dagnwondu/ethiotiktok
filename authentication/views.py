from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import update_session_auth_hash, logout, get_user_model, authenticate, login, get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import CustomUser
from . forms import UserForm
from django.contrib import messages
from django.urls import reverse
from .forms import UserUpdateForm  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Prefetch
from django.utils.timezone import now
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from livestream.models import LiveStream

#  Role based permissions
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/accounts/login/')  # no ?next=
            if request.user.user_type not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Receptionist views
# Receptionist views
# Receptionist views
@role_required(['receptionist'])
def receptionist_dashboard(request):
    today = timezone.now().date()
    return render(request, 'dashboards/receptionist_dashboard.html')
# Streamer views
# Streamer views
# Streamer views
@role_required(['streamer'])
def streamer_dashboard(request):
    # Get or create livestream for host
    livestream, created = LiveStream.objects.get_or_create(host=request.user)

    # Handle Start/Stop actions
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'start':
            livestream.is_live = True
            livestream.save()
        elif action == 'stop':
            livestream.is_live = False
            livestream.save()
        return redirect('streamer_dashboard')

    guests = livestream.guests.all()
    livestream_url = f"/media/live/{request.user.username}.m3u8"  # placeholder

    return render(request, 'dashboards/streamer_dashboard.html')
# Cashier views
# Cashier views
# Cashier views
@role_required(['cashier'])
def cashier_dashboard(request):
    return render(request, 'dashboards/cashier_dashboard.html')

# finance views
# finance views
# finance views
@role_required(['finance'])
def finance_dashboard(request):
    return render(request, 'dashboards/finance_dashboard.html')

# Doctor views
# Doctor views
# Doctor views
@role_required(['doctor'])
def doctor_dashboard(request):
    return render(request, 'dashboards/doctor_dashboard.html')

# Admin views
# Adminviews
# Adminviews
@role_required(['admin'])
def admin_dashboard(request):
    user_type = request.user.user_type
    page_header_template = f"partials/page_headers/{user_type}_header.html"
    context = {
        'page_header_template':page_header_template,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)
@login_required
def dashboard(request):
    try:
        # Get the current user's user_type
        user = CustomUser.objects.get(id=request.user.id)
        user_role = user.user_type.lower()  # e.g., "admin", "doctor", etc.
        # Redirect based on user role
        if user_role == 'streamer':
            return redirect('streamer_dashboard')
        elif user_role == 'receptionist':
            return redirect('receptionist_dashboard')
        elif user_role == 'cashier':
            return redirect('cashier_dashboard') 
        elif user_role == 'finance':
            return redirect('finance_dashboard') 
        elif user_role == 'admin':
            return redirect('admin_dashboard')
        elif user_role == 'doctor':
            return redirect('doctor_dashboard')
        elif user_role == 'nurse':
            return redirect('nurse_dashboard')
        elif user_role == 'pharmacist':
            return redirect('pharmacist_dashboard')
        elif user_role == 'lab_technologist':
            return redirect('lab_technologist_dashboard')
        elif user_role == 'accountant':
            return redirect('accountant_dashboard')
        elif user_role == 'client':
            return redirect('client_dashboard')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('/')

    # If no matching role is found
    messages.error(request, 'Unauthorized access.')
    return redirect('/')
class MyUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'users/users_management.html'
    context_object_name = 'users'
    paginate_by = 10

    # 🔐 Role restriction
    def test_func(self):
        return self.request.user.user_type == 'admin'

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to access this page.")
        return redirect('dashboard')  # change if needed

    # 📦 Extra context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('user_form', UserForm())
        return context

    # ➕ Handle user creation
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            messages.success(request, "User created successfully!")
            return redirect('users_management')

        # ❌ Form invalid
        messages.error(request, "Error while creating user.")

        self.object_list = self.get_queryset()
        context = self.get_context_data(user_form=user_form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  
            user.save()
            messages.success(request, "User created successfully!")
            return redirect('users_management')
        messages.error(request, "Error while creating User")
        self.object_list = self.get_queryset()  # Ensure object_list is set
        context = self.get_context_data()
        context['user_form'] = user_form  # Include form with errors
        return render(request, self.template_name, context)
@role_required(['admin'])
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            
            form.save()
            messages.success(request, f"'User {user} Updated Successfully'")

            return redirect("users_management")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "partials/update_user.html", {"form": form})
@role_required(['admin'])
def delete_user(request, user_id):
    # Only allow deletion if the user exists
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent deletion of yourself
    if request.user == user:
        messages.error(request, "You cannot delete yourself.")
        return redirect(reverse('users_management'))  # Update 'manage_users' with your actual view name

    # Delete the user
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect(reverse('users_management'))  # Update 'manage_users' with your actual view name
@role_required(['admin'])
def change_password(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
        else:
            messages.error(request, "Passwords do not match.")

    return redirect('users_management')  # Adjust to your URL name


@role_required(['nurse'])
def nurse_page(request):
    user = request.user
    return render(request, 'dashboard/nurse_dashboard.html')
@login_required
def logout(request):
    for sesskey in request.session.keys():
        del request.session[sesskey]
        logout(request)
        return redirect('/')  
def password_change(request):  
    return redirect('/accounts/password_change/')
# Error Pages
def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)
def custom_403(request, exception):
    return render(request, 'errors/403.html', status=403)
def custom_500(request):
    return render(request, 'errors/500.html', status=500)