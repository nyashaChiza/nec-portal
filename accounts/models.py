from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('FARMER_MANAGER', 'Farmer Manager'),
        ('DA', 'Designated Agent'),
        ('ACCOUNTANT', 'Accountant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='FARMER_MANAGER')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 

    def __str__(self):
        return f"{self.username})"
