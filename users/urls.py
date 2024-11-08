from django.urls import path
from .views import signup, verify_email

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify/<token>/', verify_email, name='verify_email'),
]
