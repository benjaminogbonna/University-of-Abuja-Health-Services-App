from django.db import models

# import in-Built User Models
from django.contrib.auth.models import User

GENDER = (
    ('f', 'Female'),
    ('m', 'Male'),
)


# Create your models here.
class Patient(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, default='')
    card_number = models.CharField(max_length=12, unique=True)
    email = models.CharField(max_length=50, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    gender = models.CharField(max_length=30, blank=True, default='')
    age = models.IntegerField(default=0, blank=True, )
    department = models.CharField(max_length=255, blank=True, default='')
    level = models.CharField(max_length=10, blank=True, default='')
    blood = models.CharField(max_length=10, blank=True, default='')
    medical_report = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return f'{self.name}, {self.username}'


class Invoice(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    outstanding = models.CharField(max_length=10)
    paid = models.CharField(max_length=10)
