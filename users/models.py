from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

import uuid


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,
                            validators=[MinLengthValidator(5)],
                            help_text="Name must be at least 5 characters")
    avatars = models.ImageField(upload_to='media/avatars', blank=True, null=True)
    is_email_validate = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name


