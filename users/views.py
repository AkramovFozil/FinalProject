from django.urls import reverse
from django.core.mail import send_mail
from .forms import CustomUserRegistrationForm
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_email_verified:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Email tasdiqlanmagan. Iltimos, emailni tasdiqlang.")
        else:
            messages.error(request, "Login yoki parol xato.")
    return render(request, 'registration/login.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Email tasdiqlanishidan oldin tizimga kira olmasin
            user.save()

            # Emailga UUID orqali xat yuborish
            verification_link = request.build_absolute_uri(
                reverse('verify_email', args=[user.email_verification_token])
            )
            send_mail(
                'Emailingizni tasdiqlang',
                f'Salom {user.username}, emailni tasdiqlash uchun shu linkga bosing: {verification_link}',
                'no-reply@example.com',
                [user.email],
                fail_silently=False,
            )
            return render(request, 'registration/signup_success.html')  # Tasdiqlash haqida xabar
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        if not user.is_email_verified:
            user.is_email_verified = True
            user.is_active = True  # Email tasdiqlanganidan keyin tizimga kirishga ruxsat beriladi
            user.save()
            return render(request, 'registration/verification_success.html')
    except CustomUser.DoesNotExist:
        return render(request, 'registration/verification_failed.html')
