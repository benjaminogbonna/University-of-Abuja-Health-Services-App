from django.contrib import admin
from PATIENT.models import Patient, Invoice
# Register your models here.


class PatientAdmin(admin.ModelAdmin):
    # fields = ['full_name', 'reg_number']
    search_fields = ['name', 'username', 'card_number']
    list_filter = ['level', 'gender']
    list_display = ['name', 'username', 'card_number', 'gender', 'level']


admin.site.register(Patient, PatientAdmin)
admin.site.register(Invoice)
