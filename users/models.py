from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
import uuid


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)],
        help_text="Ismingiz kamida 5 ta belgidan iborat bo'lishi kerak."
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.username
