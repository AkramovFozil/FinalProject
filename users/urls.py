from django.urls import path
from config import settings
from .views import HomePageView, UserLoginView, SignupView, UserLogoutView, verify_email
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
