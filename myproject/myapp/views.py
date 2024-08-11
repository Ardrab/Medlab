# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.sessions.models import Session
from .forms import RegistrationForm  # Import your RegistrationForm here
from .models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.contrib.auth.decorators import login_required

def index_view(request):
    return render(request, 'index.html')

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LabTechnician
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            print(f"User {user.email} authenticated successfully.")
            
            # Check if user is a lab technician and if their profile is completed
            if user.role == 3:  # Lab Technician
                if hasattr(user, 'lab_technicians'):
                    lab_technician = user.lab_technicians.first()
                    if lab_technician and lab_technician.profile_completed:
                        print("Redirecting completed lab tech profile to labtechindex.")
                        return redirect('labtechindex')
                    else:
                        print("Redirecting incomplete lab tech profile to labtechprofile.")
                        return redirect('labtechprofile')
            
            # Check if user is of role 2 and handle profile completion
            elif user.role == 2:  # Role 2 user
                if hasattr(user, 'profiles'):
                    user_profile = user.profiles.first()
                    if user_profile and user_profile.profile_completed:
                        print("Redirecting user with role 2 to lab index.")
                        return redirect('labindex')
                    else:
                        print("Redirecting incomplete profile user with role 2 to labprofile.")
                        return redirect('labprofile')

            # Check user role and redirect accordingly
            if user.is_superuser:
                print("Redirecting superuser to admin index.")
                return redirect('adminindex')  # Redirect to the admin index page if superuser
            elif hasattr(user, 'role'):
                if user.role == 0:
                    print("Redirecting user with role 0 to user index.")
                    return redirect('user_index')  # Redirect to the user index page if role is 0
            else:
                print("Redirecting normal user to user index.")
                return redirect('userindex')  # Redirect to the user index page if no specific role
        else:
            print("Invalid login credentials.")
            error = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')




def register_view(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 0)  # Default role to 0 if not provided

        hashed_password = make_password(password)

        user = User(
            first_name=fname,
            last_name=lname,
            username=email,
            email=email,
            password=hashed_password,
            gender=gender,
            dob=dob,
            phone=phone,
            role=role
        )
        user.save()

        # Example: Store user_id in session after registration
        request.session['user_id'] = user.id

        return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_index(request):
    return render(request, 'user/userindex.html')
def lab_index(request):
    return render(request, 'lab/labindex.html')
def labtechindex(request):
    return render(request, 'labtech/labtechindex.html')
from django.shortcuts import redirect

def logout_view(request):
    # Clear session data
    request.session.flush()

    # Perform logout action

    # Redirect to the index page
    return redirect('index')

def medicalhistory_view(request):
    return render(request, 'user/medicalhistory.html')
def adminindex_view(request):
    return render(request, 'admins/adminindex.html') 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import User

@user_passes_test(lambda u: u.is_superuser)  # Ensure only superusers can access this view
def user_list_view(request):
    # Filter users with role=0 and is_staff=False
    users = User.objects.filter(role=0, is_staff=False)
    return render(request, 'admins/user_list.html', {'users': users})
@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"User {'activated' if user.is_active else 'deactivated'} successfully.")
    return redirect('user_list')

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('user_list')
def bloodtest_view(request):
    return render(request, 'user/blood.html')
def urinetest_view(request):
    return render(request, 'user/urine.html')
def swabtest_view(request):
    return render(request, 'user/swab.html')
import secrets
import string
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

def addlab_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        role = request.POST.get('role')  # Get role value from hidden input

        User = get_user_model()
        if User.objects.filter(username=email).exists():
            messages.error(request, "Username (email) already exists.")
            return render(request, 'admins/addlab.html')

        # Generate a random password
        random_password = generate_random_password()

        # Create a new user
        user = User(
            first_name=first_name,
            username=email,  # Use username field for email
            email=email,
            role=role,
            password=make_password(random_password)
        )

        # Save the user
        user.save()

        # Send email with the autogenerated password
        subject = 'Your Account Details for MEDLAB'
        message = f'Hello {first_name},\n\nYour account has been created successfully. Here are your login details:\n\nEmail: {email}\nPassword: {random_password}\n\nPlease change your password after logging in.\n\nBest regards,\nMEDLAB Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            messages.error(request, "Failed to send email with the autogenerated password.")

        messages.success(request, "User added successfully. The autogenerated password has been sent to the provided email address.")
        return redirect('adminindex')

    return render(request, 'admins/addlab.html')




import time
import sqlite3
from django.db import transaction

def addlabtech_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        role = request.POST.get('role')  # Get role value from hidden input

        User = get_user_model()
        if User.objects.filter(username=email).exists():
            messages.error(request, "Username (email) already exists.")
            return render(request, 'lab/addlabtech.html')

        # Generate a random password
        random_password = generate_random_password()

        retries = 5
        while retries > 0:
            try:
                with transaction.atomic():
                    # Create a new user
                    user = User(
                        first_name=first_name,
                        last_name=lname,
                        username=email,  # Use username field for email
                        email=email,
                        role=role,
                        password=make_password(random_password)
                    )
                    # Save the user
                    user.save()
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retries -= 1
                    time.sleep(1)  # Wait for a second before retrying
                else:
                    raise

        if retries == 0:
            messages.error(request, "Failed to add user due to a database lock.")
            return render(request, 'lab/addlabtech.html')

        # Send email with the autogenerated password
        subject = 'Your Account Details for MEDLAB'
        message = f'Hello {first_name},\n\nYour account has been created successfully. Here are your login details:\n\nEmail: {email}\nPassword: {random_password}\n\nPlease change your password after logging in.\n\nBest regards,\nMEDLAB Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            messages.error(request, "Failed to send email with the autogenerated password.")

        messages.success(request, "User added successfully. The autogenerated password has been sent to the provided email address.")
        return redirect('labindex')

    return render(request, 'lab/addlabtech.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

@login_required
def profile_view(request):
    return render(request, 'user/profile_view.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        # Get updated data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')

        # Update the user object
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.gender = gender
        user.dob = dob
        user.phone = phone

        # Save the updated user object
        user.save()

        # Redirect to the profile view or another page
        return redirect('profile')  # Adjust this redirect as needed

    return render(request, 'user/edit_profile.html', {'user': user})
from django.shortcuts import render
from .models import User, UserProfile  # Adjust the import based on your project structure

def labtech_list_view(request):
    # Filter users by role=2 and prefetch related UserProfile data
    users = User.objects.filter(role=2).prefetch_related('profiles')
    return render(request, 'admins/labtech.html', {'users': users})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserProfileForm
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from .models import UserProfile
from .forms import UserProfileForm

User = get_user_model()

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
def labprofile_view(request):
    if request.method == 'POST':
        # Extract form data from POST request
        license_number = request.POST.get('license_number')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Get the currently logged-in user
        user = request.user

        if not user.is_authenticated:
            messages.error(request, 'User is not authenticated')
            return redirect('login')  # Redirect to login if user is not authenticated

        # Check if passwords match and update the password if provided
        if password:
            if password == confirm_password:
                user.set_password(password)  # Use set_password to hash the password
                user.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('labprofile')  # Redirect back to the form

        # Update or create the UserProfile
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'city': city,
                'phone_no': phone,
                'license_no': license_number,
                'profile_completed': True
            }
        )

        messages.success(request, 'User profile updated successfully')
        return redirect('labindex')  # Redirect to labindex after saving profile

    else:
        # Try to get the user's UserProfile or initialize an empty form
        try:
            profile = request.user.profiles.first()  # Changed to access UserProfile via profiles
            form = UserProfileForm(instance=profile)
        except UserProfile.DoesNotExist:
            form = UserProfileForm()

    return render(request, 'lab/labprofile.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from .models import LabTechnician
from .forms import LabTechnicianForm

User = get_user_model()

@login_required
def labtechprofile_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        specialization = request.POST.get('specialization')

        # Get the currently logged-in user
        user = request.user

        if not user.is_authenticated:
            messages.error(request, 'User is not authenticated')
            return redirect('login')

        # Update the user's password if provided
        if password:
            if password == confirm_password:
                user.set_password(password)
                update_session_auth_hash(request, user)  # Update session hash to prevent logout
                user.save()  # Save user with updated password
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('labtechprofile')

        # Update user's dob, gender, and phone using update_or_create
        user.dob = dob if dob else user.dob
        user.gender = gender if gender else user.gender
        user.phone = phone if phone else user.phone
        user.save()

        # Update or create LabTechnician profile
        LabTechnician.objects.update_or_create(
            user=user,
            defaults={
                'specialization': specialization,
                'profile_completed': True
            }
        )

        messages.success(request, 'User profile updated successfully')
        return redirect('labtechindex')

    else:
        # Try to get the user's LabTechnician profile or initialize an empty form
        try:
            lab_technician = request.user.lab_technicians.first()
            form = LabTechnicianForm(instance=lab_technician)
        except LabTechnician.DoesNotExist:
            form = LabTechnicianForm()

    return render(request, 'labtech/labtechprofile.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestName, UserProfile  # Ensure your models are imported

def addtest_view(request):
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        if test_name:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                new_test_name = TestName(test_name=test_name, lad_id=user_profile)
                new_test_name.save()
                messages.success(request, 'Test name added successfully!')
                return redirect('labindex')  # Redirect to the lab index page after saving
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile does not exist.')
                return redirect('addtest')  # Redirect to the lab index page
        else:
            messages.error(request, 'Please enter a test name.')
    
    return render(request, 'lab/addtest.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestName, Tests

def addtestname_view(request):
    if request.method == 'POST':
        test_type_names = request.POST.get('test_type_names')
        name_id = request.POST.get('name_id')
        
        if test_type_names and name_id:
            try:
                test_name = TestName.objects.get(pk=name_id)
                new_test = Tests(name_id=test_name, test_type_names=test_type_names)
                new_test.save()
                messages.success(request, 'Test added successfully!')
                return redirect('labindex')  # Redirect to the lab index page after saving
            except TestName.DoesNotExist:
                messages.error(request, 'Invalid Test Name ID.')
        else:
            messages.error(request, 'All fields are required.')
    
    test_names = TestName.objects.all()
    return render(request, 'lab/addtestname.html', {'test_names': test_names})

from django.shortcuts import render, redirect
from .models import Tests, TestType

# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestType, Tests



   # myapp/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TestType, Tests

def add_test_types(request):
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        tests_names = request.POST.get('tests_names')
        normal_range = request.POST.get('normal_range')

        if test_id and tests_names and normal_range:
            try:
                test = Tests.objects.get(test_id=test_id)
                test_type = TestType(test_id=test, tests_names=tests_names, normal_range=normal_range)
                test_type.save()
                messages.success(request, 'Test type added successfully')
                return redirect('labindex')  # Adjust this redirect URL as needed
            except Tests.DoesNotExist:
                messages.error(request, 'Selected test does not exist.')
        else:
            messages.error(request, 'All fields are required.')

    test_names = Tests.objects.all()
    return render(request, 'lab/addtesttypes.html', {'test_names': test_names})


from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.http import HttpResponse
from django.urls import reverse

User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the uidb64 and get the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Invalid password reset link')

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Extract new password and confirm password from POST data
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            print(f"New password: {new_password}")
            print(f"Confirm password: {confirm_password}")

            if new_password and new_password == confirm_password:
                # Set the new password directly
                user.set_password(new_password)
                user.save()

                print("Password updated successfully")

                # Important to update session auth hash after password change
                update_session_auth_hash(request, user)

                return redirect('password_reset_complete')
            else:
                return render(request, 'password_reset_confirm.html', {'error': 'Passwords do not match.'})
        else:
            # Display the form to enter new password
            return render(request, 'password_reset_confirm.html')
    else:
        return HttpResponse('Invalid password reset link')




from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_body = render_to_string(email_template_name, c)
                    send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return redirect('password_reset_done')
    else:
        # Display the password reset request form
        return render(request, 'password_reset.html', {'password_reset': True})
def password_reset_complete(request):
    return render(request, 'password_reset_complete.html', {'reset_complete': True})
def password_reset_done(request):
    return render(request, 'password_reset_done.html', {'reset_done': True})
    
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TestName, Tests, TestType
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TestName, Tests, TestType
from django.views.decorators.csrf import csrf_exempt

# View to render the form
def add_test_type_view(request):
    test_names = TestName.objects.all()
    return render(request, 'add_test_type.html', {'test_names': test_names})

# View to handle fetching test types by TestName ID
def get_test_types_by_name(request, name_id):
    tests = Tests.objects.filter(name_id=name_id)
    data = {'test_types': [{'test_id': test.test_id, 'test_type_names': test.test_type_names} for test in tests]}
    return JsonResponse(data)

# View to handle fetching tests by TestType ID
def get_tests_by_type(request, test_id):
    test_type = get_object_or_404(Tests, pk=test_id)
    test_types = TestType.objects.filter(test_id=test_type)
    data = {'tests': [{'tests_names': test_type.tests_names} for test_type in test_types]}
    return JsonResponse(data)

# View to handle form submission


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from .models import Tests, Booking, TestName

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from .models import Booking, Tests, TestName

@login_required
def add_test_type(request):
    if request.method == 'POST':
        # Extract data from the POST request
        test_id=request.POST.get('test_id')
        name_id = request.POST.get('name_id')
        test_ids = request.POST.getlist('test_ids')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Debug statements to verify data
        print("TE ID:", test_id)
        print("Name ID:", name_id)
        print("Test IDs:", test_ids)
        print("Appointment Date:", appointment_date)
        print("Appointment Time:", appointment_time)

        # Basic validation
        if not name_id or not appointment_date or not appointment_time:
            return HttpResponse("Required fields are missing.")
        
        # Convert 12-hour time format (if needed) to 24-hour time format
        if appointment_time:
            appointment_time_24 = datetime.strptime(appointment_time, '%I:%M %p').strftime('%H:%M')
        else:
            return HttpResponse("Invalid time format. Please use 'HH:MM AM/PM'.")

        # Combine date and time into a single datetime
        if appointment_date and appointment_time_24:
            appointment_datetime = datetime.combine(
                datetime.strptime(appointment_date, '%Y-%m-%d').date(),
                datetime.strptime(appointment_time_24, '%H:%M').time()
            )
        else:
            return HttpResponse("Invalid date or time format.")

        # Create and save a new Booking
        booking = Booking(
            user=request.user,
            appointment_date=appointment_datetime,
            appointment_time=appointment_time_24,  # Store time in 24-hour format
            status='pending',  # Default status
            test_id=name_id  # Set the test type based on the name_id
        )
        booking.save()

        # Optionally, handle additional test types if necessary
        for test_id in test_ids:
            test = Tests.objects.filter(test_id=test_id).first()
            if test:
                # Handle saving TestType information or associate it with the booking if needed
                pass

        # Redirect to userindex after successful form submission
        return redirect('user_index')
    
    else:
        # For GET requests, render the form
        test_names = TestName.objects.all()
        return render(request, 'user/add_test_type.html', {'test_names': test_names})

from django.shortcuts import render, get_object_or_404
from .models import Booking
from .forms import BookingForm



from django.shortcuts import render, get_object_or_404
from .models import Booking, TestType

def booking_list_view(request):
    bookings = Booking.objects.all()
    return render(request, 'lab/booking_detail.html', {'bookings': bookings})

from django.shortcuts import render
from django.http import HttpResponse

def schedule_xray_view(request):
    
    # Render the form template
    return render(request, 'schedule-xray.html')
@login_required
def update_booking_status(request, booking_id, new_status):
    booking = get_object_or_404(Booking, id=booking_id)

    # Ensure the new_status is valid
    if new_status in dict(Booking.STATUS_CHOICES):
        booking.status = new_status
        booking.save()
        return redirect('booking_list_view')
    else:
        return HttpResponse("Invalid status.")
