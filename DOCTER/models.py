from django.db import models
from PATIENT.models import *
from .models import *
from COMMON_APP.models import *
# Create your models here.
from django.contrib.auth.models import User


# Create your models here.
class Docter(models.Model):
	username = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=40, blank=True, default='')
	phone = models.CharField(max_length=12, default="",blank=True)
	email = models.CharField(max_length=50, blank=True, default='')
	gender = models.CharField(max_length=30, blank=True, default='')
	address = models.CharField(max_length=200, blank=True, default='')
	status = models.BooleanField(default=0)
	department = models.CharField(max_length=30, blank=True, default='')

	def __str__(self):
		return f'{self.name}'

	
# Prescription Model


class Prescription2(models.Model):
	prescription = models.CharField(max_length=200)
	symptoms = models.CharField(max_length=200)
	patient = models.ForeignKey(Patient,on_delete = models.CASCADE,unique = False)
	docter = models.ForeignKey(Docter,on_delete = models.CASCADE,unique = False)
	appointment = models.ForeignKey('COMMON_APP.Appointment',on_delete = models.CASCADE,unique = False)
	prescripted_date = models.DateField(auto_now = True) 
	outstanding = models.IntegerField(default = 0)
	paid = models.IntegerField(default = 0)
	total = models.IntegerField(default = 0)


# HR Dashboard Data