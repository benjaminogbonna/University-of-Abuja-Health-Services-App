from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
from django import template
from django.template.loader import get_template
from io import BytesIO
import xhtml2pdf.pisa as pisa
from .utils import render_to_pdf  # created in step 4
from django.db import IntegrityError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from DOCTER.models import *
from PATIENT.models import *
from COMMON_APP.models import *
from Application_Main.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request, 'home.html', {"user": None})


def about(request):
    status = False
    if request.user:
        status = request.user
    return render(request, 'about.html')


def staff(request):
    return render(request, 'staff.html')


def contact(request):
    status = False
    if request.user:
        status = request.user
    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])

            return render(request, 'register.html')
        except User.DoesNotExist:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['pass1'])
            if request.POST['post'] == 'Patient':
                new = Patient(phone=request.POST['phone'], name=request.POST['name'], email=request.POST['email'],
                              username=user)
                new.save()

                c_patient = Invoice(patient=new, outstanding=0, paid=0)
                c_patient.save()

                return render(request, 'register.html')
            else:
                new = Docter(phone=request.POST['phone'], name=request.POST['name'], email=request.POST['email'],
                             username=user)
                new.save()
                return render(request, 'register.html')

            return render(request, 'register.html')
    else:
        return render(request, 'register.html')


# Login
def login(request):
    if request.method == 'POST':
        try:
            # Check User in DB
            uname = request.POST['username']
            pwd = request.POST['pass1']
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            # if request.user.is_is_authenticated:
            if user_authenticate != None:
                user = User.objects.get(username=uname)
                try:
                    data = Patient.objects.get(username=user)
                    auth.login(request, user_authenticate)
                    return redirect('profile', user="P")
                except:
                    try:
                        data = Docter.objects.get(username=user)
                        auth.login(request, user_authenticate)
                        return redirect('profile', user="D")
                    except:
                        try:
                            data = Receptionist.objects.get(username=user)
                            auth.login(request, user_authenticate)
                            return redirect('receptionist_dashboard', user="R")
                        except:
                            try:
                                data = HR.objects.get(username=user)
                                auth.login(request, user_authenticate)
                                return redirect('hr_dashboard', user="H")
                            except:
                                return redirect('/')

            else:
                return render(request, 'login.html')
        except:
            return render(request, 'login.html')
    return render(request, 'login.html')


# Logout
def logout(request):
    auth.logout(request)
    return redirect('home')


# Profile
@login_required()
def profile(request, user):
    userid = User.objects.get(username=request.user)
    status = False
    if request.user:
        status = request.user
    if request.method == "POST":
        if user == "P":
            update = Patient.objects.get(username=userid)
            # update.name = request.POST['name']
            update.phone = request.POST['phone']
            update.email = request.POST['email']
            update.gender = request.POST['gender']
            update.age = request.POST['age']
            update.blood = request.POST['blood']
            update.address = request.POST['address']
            update.department = request.POST['department']
            update.level = request.POST['level']
            try:
                myfile = request.FILES['report']
                fs = FileSystemStorage(location='media/report/')
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)
                update.medical = url
            except:
                pass
            update.save()
            return redirect('profile', user=user)
        else:
            update = Docter.objects.get(username=userid)
            update.name = request.POST['name']
            update.phone = request.POST['phone']
            update.email = request.POST['email']
            update.gender = request.POST['gender']
            update.address = request.POST['address']
            update.department = request.POST['department']
            update.save()
            return redirect('profile', user=user)

    if user == "P":
        userdata = Patient.objects.get(username=userid)
        return render(request, 'patient_profile.html', {'userdata': userdata, 'user': user, "status": status})

    else:
        userdata = Docter.objects.get(username=userid)
        return render(request, 'docter_profile.html', {'userdata': userdata, 'user': user, "status": status})

    # elif user == 'H':
    #     userdata = HR.objects.get(username=userid)
    #     return render(request, 'hr_dashboard.html', {'userdata': userdata, 'user': user, "status": status})

    return redirect('/')


@login_required()
def dashboard(request, user):
    status = False
    if request.user:
        status = request.user
    if user == "AnonymousUser":
        return redirect('home')

    return render(request, 'patient_profile.html', {'user': user, "status": status})


@login_required()
def receptionist_dashboard(request, user):
    status = False
    if request.user:
        status = request.user
    row = Appointment.objects.all().order_by('-pk')
    total_doctors = len(Docter.objects.all())
    total_patients = len(Patient.objects.all())
    status_done = len(Appointment.objects.filter(status=1))
    status_pending = len(row) - status_done
    all_patient = Patient.objects.all().order_by('-pk')
    context = {'user': user,
               "status": status,
               "Total": len(row),
               "Done": status_done,
               "Pending": status_pending,
               'all_data': row,
               'all_patient': all_patient,
               'total_patients': total_patients,
               'total_doctors': total_doctors,
               }
    return render(request, 'receptionist_dashboard.html', context)


@login_required()
def hr_dashboard(request, user):
    status = False
    if request.user:
        status = request.user
    all_p = Patient.objects.all()
    all_d = Docter.objects.all()
    active_d = Docter.objects.filter(status=1)
    context = {'user': user,
               "all_p": len(all_p),
               "all_d": len(all_d),
               "all_data": all_d,
               "active_d": len(active_d),
               'status': status
               }
    return render(request, 'hr_dashboard.html', context)

def create_appointment(request, user):
    status = False
    if request.user:
        status = request.user

    if request.method == "POST":
        d_id = int(request.POST['docter'])
        p_id = int(request.POST['patient'])

        docter = Docter.objects.get(pk=d_id)
        patient = Patient.objects.get(pk=p_id)

        p_id = int(request.POST['patient'])
        status = int(request.POST['status'])
        new_appointment = Appointment(docterid=docter, patientid=patient, time=request.POST['time'],
                                      date=request.POST['date'], status=status)
        new_appointment.save()
        return redirect('receptionist_dashboard', user="R")

    patient_names = Patient.objects.all()
    doctor_names = Docter.objects.all()
    context = {'user': user,
               "status": status,
               "patient_names": patient_names,
               "doctor_names": doctor_names
               }

    return render(request, 'create_appointment.html', context)


# Delete Patient
def delete_patient(request, id):
    data = Patient.objects.get(id=id)
    data.delete()
    return redirect('receptionist_dashboard', user="R")


# Create Patient => Receptionist
def create_patient(request):
    status = False
    if request.user:
        status = request.user
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            print(user)
            return redirect('receptionist_dashboard', user="R")
        except User.DoesNotExist:
            user = User.objects.create_user(username=request.POST['username'], password='default')
            try:
                myfile = request.FILES['report']
                fs = FileSystemStorage(location='media/report/')
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)

            except:
                url = ""
            new = Patient(username=user,
                          # username=request.POST['username'],
                          name=request.POST['name'],
                          card_number=request.POST['card_number'],
                          email=request.POST['email'],
                          phone=request.POST['phone'],
                          gender=request.POST['gender'],
                          age=request.POST['age'],
                          blood=request.POST['blood'],
                          department=request.POST['department'],
                          level=request.POST['level'],
                          address=request.POST['address'],
                          medical_report=url,
                          )
            new.save()
            print(new)

            c_patient = Invoice(patient=new, outstanding=2, paid=5)
            c_patient.save()
            return redirect('receptionist_dashboard', user="R")
    users = User.objects.all().order_by('-pk')
    context = {'user': "R",
               'status': status,
               'users': users}
    return render(request, 'create_patient.html', context)


# Update Patient=> Receptionist
def update_patient(request, id):
    status = False
    if request.user:
        status = request.user
    if request.method == "POST":
        update = Patient.objects.get(id=id)
        update.name = request.POST['name']
        update.phone = request.POST['phone']
        update.email = request.POST['email']
        update.gender = request.POST['gender']
        update.age = request.POST['age']
        update.blood = request.POST['blood']
        update.address = request.POST['address']
        update.case = request.POST['case']
        try:
            myfile = request.FILES['report']
            fs = FileSystemStorage(location='media/report/')
            filename = fs.save(myfile.name, myfile)
            # print(name,file)
            url = fs.url(filename)
            print(url)
            update.medical = url
        except:
            pass
        update.save()
        extra_update = Invoice.objects.get(patient=update)

        extra_update.outstanding = request.POST['outstanding']
        extra_update.paid = request.POST['paid']
        extra_update.save()
        return redirect('receptionist_dashboard', user="R")
    data = Patient.objects.get(id=id)
    extra = Invoice.objects.get(patient=data)
    return render(request, 'update_patient.html', {'data': data, 'extra': extra, 'user': "R", 'status': status})


def myappointment(request):
    status = False
    if request.user:
        status = request.user
    user_id = User.objects.get(username=request.user)
    patient = Patient.objects.get(username=user_id)
    data = Appointment.objects.filter(patientid=patient)
    return render(request, 'my_appointment.html', {'data': data, 'user': "P", 'status': status})


def docter_appointment(request):
    status = False
    if request.user:
        status = request.user
    user_id = User.objects.get(username=request.user)
    docter = Docter.objects.get(username=user_id)
    data = Appointment.objects.filter(docterid=docter)

    return render(request, 'my_appointment.html', {'data': data, 'user': "D", 'status': status})


def docter_prescription(request):
    status = False
    if request.user:
        status = request.user
    user_id = User.objects.get(username=request.user)
    docter = Docter.objects.get(username=user_id)
    print(docter)
    pers = Prescription2.objects.filter(docter=docter)
    print(len(pers))
    for i in pers:
        print(i.patient)
    return render(request, 'docter_prescription.html', {'pers': pers, 'user': "D", 'status': status})


# Create Prescription 
def create_prescription(request):
    status = False
    if request.user:
        status = request.user
    if request.method == 'POST':
        appointment = Appointment.objects.get(id=request.POST['appointment'])

        user_id = User.objects.get(username=request.user)
        docter = Docter.objects.get(username=user_id)
        new_prescrition = Prescription2(symptoms=request.POST['symptoms'], prescription=request.POST['prescription'],
                                        patient=appointment.patientid, docter=docter, appointment=appointment)
        new_prescrition.save()
        return redirect('docter_prescription')
    user_id = User.objects.get(username=request.user)
    docter = Docter.objects.get(username=user_id)
    data = Appointment.objects.filter(docterid=docter, status=0)
    print(data)

    return render(request, 'create_prescription.html', {"data": data, 'user': "D", 'status': status})


def medical_history(request):
    status = False
    if request.user:
        status = request.user
    user_id = User.objects.get(username=request.user)
    print(user_id)
    patient = Patient.objects.get(username=user_id)
    data = Prescription2.objects.filter(patient=patient)
    print(data)
    return render(request, 'medical_history.html', {"data": data, 'user': "P", 'status': status})


def update_status(request, id):
    print(id)
    status = False
    if request.user:
        status = request.user
    if request.method == "POST":
        data = Appointment.objects.get(id=id)
        pers = Prescription2.objects.get(appointment=data)
        pers.outstanding = request.POST['outstanding']
        pers.paid = request.POST['paid']
        pers.total = int(request.POST['outstanding']) + int(request.POST['paid'])
        pers.save()
        data.status = 1
        data.save()
        return redirect('receptionist_dashboard', user="R")

    return render(request, 'update_status.html', {'user': "R", "id": id, 'status': status})


@login_required()
# def hr_dashboard(request):
#     status = False
#     if request.user:
#         status = request.user
#     all_p = Patient.objects.all()
#     all_d = Docter.objects.all()
#     active_d = Docter.objects.filter(status=1)
#     return render(request, 'hr_dashboard.html',
#                   {"all_p": len(all_p), "all_d": len(all_d), "all_data": all_d, "active_d": len(active_d), 'user': "H",
#                    'status': status})


def update_docter(request, id):
    status = False
    if request.user:
        status = request.user
    if request.method == "POST":
        update = Docter.objects.get(id=id)
        update.name = request.POST['name']
        update.phone = request.POST['phone']
        update.email = request.POST['email']
        update.gender = request.POST['gender']
        update.age = request.POST['age']
        update.blood = request.POST['blood']
        update.address = request.POST['address']
        update.department = request.POST['department']
        update.salary = request.POST['salary']
        update.status = request.POST['status']
        update.attendance = request.POST['attendance']
        update.save()
        return redirect('hr_dashboard')
    data = Docter.objects.get(id=id)
    return render(request, 'update_docter.html', {"userdata": data, 'user': "H", 'status': status})


def delete_docter(request):
    return HttpResponse('<h2 style="color:red">You are Not authorized</h2>')


def hr_accounting(request):
    status = False
    if request.user:
        status = request.user
    individual = Invoice.objects.all()
    consulation = Prescription2.objects.all()

    return render(request, 'hr_accounting.html',
                  {'individual': individual, 'consulation': consulation, 'user': 'H', 'status': status})


def patient_invoice(request):
    status = False
    if request.user:
        status = request.user
    user_id = User.objects.get(username=request.user)
    p = Patient.objects.get(username=user_id)
    data = Prescription2.objects.filter(patient=p)
    return render(request, 'patient_invoice.html', {'data': data, 'user': 'P', 'status': status})


def get_pdf(request, id):
    data = Prescription2.objects.get(id=id)
    pdf_data = {'data': data}
    template = get_template('invoice.html')
    data_p = template.render(pdf_data)
    response = BytesIO()
    pdf_page = pisa.pisaDocument(BytesIO(data_p.encode('UTF_8')), response)
    if not pdf_page.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')


def send_reminder(request, id):
    p = Prescription2.objects.get(id=id)
    email = p.patient.email
    subject = 'Payment Reminder '
    message = 'Your Due Amount is {} outstanding and {} rs. you have already paid'.format(p.outstanding, p.paid)
    recepient = [email]
    send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently=False)
    return redirect('hr_accounting')
