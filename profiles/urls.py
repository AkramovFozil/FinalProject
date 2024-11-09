from django.urls import path
from .views import user_profile, edit_profile, my_profile

urlpatterns = [
    path('<str:username>/', user_profile, name='user_profile'),
    path('<str:username>/edit/', edit_profile, name='edit_profile'),
    path('my_profile/', my_profile, name='my_profile'),
]
