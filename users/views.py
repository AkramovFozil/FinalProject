from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import CustomUserRegistrationForm
from .models import CustomUser


# Home Page View
class HomePageView(TemplateView):
    template_name = 'index-without-login.html'


# User Login View
class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Login yoki parol xato.")
        return super().form_invalid(form)

    def form_valid(self, form):
        # Check if the user's email is verified
        user = form.get_user()
        if not user.is_email_verified:
            messages.error(self.request, "Email tasdiqlanmagan. Iltimos, emailni tasdiqlang.")
            return redirect('login')
        return super().form_valid(form)


class SignupView(FormView):
    template_name = 'register.html'
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Foydalanuvchi email tasdiqlanmaguncha faollashtirilmaydi
        user.save()

        # Tasdiqlash emailini yuborish
        verification_link = self.request.build_absolute_uri(
            reverse('verify_email', args=[user.email_verification_token])
        )
        send_mail(
            'Emailingizni tasdiqlang',
            f'Salom {user.username}, emailni tasdiqlash uchun quyidagi linkga bosing: {verification_link}',
            'no-reply@example.com',
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, "Ro'yxatdan o'tish muvaffaqiyatli. Iltimos, emailni tasdiqlang.")
        return redirect('login')


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        if not user.is_email_verified:
            user.is_email_verified = True
            user.is_active = True
            user.save()
            messages.success(request, "Email muvaffaqiyatli tasdiqlandi.")
            return redirect('login')
    except CustomUser.DoesNotExist:
        messages.error(request, "Xato! Tasdiqlash tokeni noto'g'ri.")
        return redirect('signup')


class UserLogoutView(LogoutView):
    template_name = 'index-without-login.html'
