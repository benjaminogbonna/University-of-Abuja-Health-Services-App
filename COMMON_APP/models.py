from django.db import models
from django.contrib.auth.models import User
from DOCTER.models import *
from PATIENT.models import *
# Create your models here.


# Model For Receptionist
class Receptionist(models.Model):
	username = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=40, blank=True, default='')
	email = models.CharField(max_length=50, blank=True, default='')
	phone = models.CharField(max_length=12, blank=True, default='')
	address = models.CharField(max_length=200, blank=True, default='')

	def __str__(self):
		return f'{self.name}, {self.username}'


# Model For Appointment
class Appointment(models.Model):
	docterid = models.ForeignKey('DOCTER.Docter', on_delete=models.CASCADE)
	patientid = models.ForeignKey('PATIENT.Patient', on_delete=models.CASCADE)
	time = models.TimeField()
	date = models.DateField(default="")
	status = models.BooleanField(max_length=15, default=0)

	def __str__(self):
		return f'Appointment for: Dr {self.docterid} and {self.patientid}'


# Model For HR
class HR(models.Model):
	username = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=40)
	email = models.CharField(max_length=50, blank=True, default='')
	phone = models.CharField(max_length=12, blank=True, default='')
	address = models.CharField(max_length=200, blank=True, default='')

	def __str__(self):
		return f'{self.name}, {self.username}'
