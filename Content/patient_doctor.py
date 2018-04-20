from datetime import timedelta

import pytz
from django.db.models import Q
from rest_framework.decorators import api_view

from Content.models import Patient, Doctor, Appointments
import string
import random, uuid
from django.utils import timezone
import dateutil.parser


def add_patient(data):
    if data['photo_url'] == "":
        data['photo_url'] = "https://themes.gohugo.io/theme/hugo-geo//img/profile.png"
    patient_obj = Patient(name=data['name'], age=data['age'], email_id=data['email_id'],
                          contact_no=data['contact_no'], photo_url=data['photo_url'])
    patient_obj.save()


def update_patient(data, pid):
    if Patient.objects.filter(contact_no=pid).exists():
        patient_obj = Patient.objects.get(contact_no=pid)

        patient_obj.name = data['name']
        patient_obj.age = data['age']
        patient_obj.email_id = data['email_id']
        patient_obj.password = data['password']
        patient_obj.contact_no = data['contact']

        patient_obj.save()


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_doctor(data):
    if data["independent_doctor"] == 'yes':
        data["independent_doctor"] = True
    else:
        data["independent_doctor"] = False

    if data['photo_url'] == "":
        data['photo_url'] = "https://cdn2.iconfinder.com/data/icons/rcons-user/32/male-shadow-fill-circle-512.png"
    doctor_obj = Doctor(name=data['name'], fees=data['fees'], email_id=data['email_id'],
                        contact_no=data['contact_no'], speciality=data['speciality'], age=data['age'],
                        experience=data['experience'], degree=data['degree'], doctor_terminal_login=id_generator(6),
                        doctor_terminal_password=data['password'],photo_url=data['photo_url'],
                        independent_doctor=data['independent_doctor'], address=data['address'])
    print("ok")
    doctor_obj.save()


def update_doctor(data, d_id):
    if Doctor.objects.filter(contact_no=d_id).exists():
        doctor_obj = Doctor.objects.get(contact_no=d_id)

        doctor_obj.name = data['name']
        doctor_obj.age = data['age']
        doctor_obj.email_id = data['email_id']
        doctor_obj.password = data['password']
        doctor_obj.contact_no = data['contact']
        doctor_obj.speciality = data['speciality']
        doctor_obj.fees = data['fees']
        doctor_obj.save()


def get_appointments(p_id):
    appointments_list = Patient.objects.get(contact_no=p_id).appointment_list.order_by('on_date')
    local_tz = pytz.timezone('Asia/Kolkata')
    appointments_dict = dict()
    items = []
    for appointment in appointments_list:
        appointment_dict = dict()
        appointment_dict['doctor_name'] = Doctor.objects.get(contact_no=appointment.doctor_id).name
        appointment_dict['doctor_address'] = Doctor.objects.get(contact_no=appointment.doctor_id).address
        appointment_dict['status'] = appointment.status
        appointment_dict['on_date'] = appointment.on_date
        appointment_dict['doctor_photo'] = Doctor.objects.get(contact_no=appointment.doctor_id).photo_url
        appointment_dict['appointment_id'] = appointment.appointment_id
        time = timezone.now().astimezone(local_tz).replace(hour=10, second=00, minute=00, microsecond=0)
        est1 = time + timedelta(minutes=15 * appointment.booking_no)
        est2 = appointment.booked_on
        if est2 > est1:
            a = est2 + timedelta(minutes=15)
        else:
            a = est1
        appointment_dict['estimated_time'] = a
        appointment_dict['booking_no'] = appointment.booking_no
        appointment_dict['open'] = True
        appointment_dict['current_no'] = Doctor.objects.get(contact_no=appointment.doctor_id).current_appointment_no
        if appointment.on_date < timezone.now().astimezone(local_tz).date():
            appointment_dict['open'] = False
            appointment_dict['current_no'] = 0
        # appointment_dict['current_no'] =
        if appointment.on_date > timezone.now().astimezone(local_tz).date():
            appointment_dict['current_no'] = 0
        if appointment.status == "done":
            appointment_dict['open'] = False
            appointment_dict['current_no'] = 0

        items.append(appointment_dict)

    appointments_dict['items'] = items
    return appointments_dict


def get_filtered_doctor_list(query):
    doctor_list = Doctor.objects.filter(
        Q(name__icontains=query) | Q(degree__icontains=query) | Q(
            speciality__icontains=query) | Q(address__icontains=query))

    doctors_dict = dict()
    items = []
    for doctor in doctor_list:
        doctor_dict = dict()
        doctor_dict['doctor_name'] = doctor.name
        doctor_dict['doctor_address'] = doctor.address
        doctor_dict['fees'] = doctor.fees
        doctor_dict['speciality'] = doctor.speciality
        doctor_dict['independent'] = doctor.independent_doctor
        doctor_dict['contact'] = doctor.contact_no
        doctor_dict['email_id'] = doctor.email_id
        doctor_dict['photo'] = doctor.photo_url
        doctor_dict['degree'] = doctor.degree

        items.append(doctor_dict)

    doctors_dict['items'] = items
    return doctors_dict


def book_appointments(data):
    d_id = data['d_id']
    p_id = data['p_id']
    local_tz = pytz.timezone('Asia/Kolkata')
    appointment_date = dateutil.parser.parse(data['appointment_date']).astimezone(local_tz).date()
    current_dateTime = timezone.now().astimezone(local_tz)

    booking_no = Doctor.objects.get(contact_no=d_id).appointment_list.filter(on_date=appointment_date).count() + 1
    appointment = Appointments(appointment_id=uuid.uuid4(), patient_id=p_id, doctor_id=d_id, status='Booked',
                               on_date=appointment_date, fees_paid=data['fees_paid'], booked_on=current_dateTime,
                               booking_no=booking_no)

    appointment.save()

    patient = Patient.objects.get(contact_no=p_id)
    patient.appointment_list.add(appointment)
    patient.save()
    doctor = Doctor.objects.get(contact_no=d_id)
    doctor.appointment_list.add(appointment)
    doctor.save()


def doctor_get_todayappointment_list(data):
    local_tz = pytz.timezone('Asia/Kolkata')
    doctor = Doctor.objects.get(contact_no=data['doctor_id'])
    appointments_list = doctor.appointment_list.filter(on_date=timezone.now().astimezone(local_tz).date()).order_by(
        'booked_on')
    response_dict = dict()
    items = []

    for appointment in appointments_list:
        appointment_dict = dict()
        appointment_dict['patient_name'] = Patient.objects.get(contact_no=appointment.patient_id).name
        appointment_dict['patient_age'] = Patient.objects.get(contact_no=appointment.patient_id).age
        appointment_dict['patient_contact'] = Patient.objects.get(contact_no=appointment.patient_id).contact_no
        appointment_dict['patient_photo'] = Patient.objects.get(contact_no=appointment.patient_id).photo_url
        appointment_dict['status'] = appointment.status
        items.append(appointment_dict)

    response_dict["items"] = items

    return response_dict


def doctor_get_futureappointment_list(data):
    local_tz = pytz.timezone('Asia/Kolkata')
    doctor = Doctor.objects.get(contact_no=data['doctor_id'])
    appointments_list = doctor.appointment_list.filter(on_date__gt=timezone.now().astimezone(local_tz).date()).order_by(
        'booked_on')
    response_dict = dict()
    items = []

    for appointment in appointments_list:
        appointment_dict = dict()
        appointment_dict['patient_name'] = Patient.objects.get(contact_no=appointment.patient_id).name
        appointment_dict['patient_age'] = Patient.objects.get(contact_no=appointment.patient_id).age
        appointment_dict['patient_contact'] = Patient.objects.get(contact_no=appointment.patient_id).contact_no
        appointment_dict['patient_photo'] = Patient.objects.get(contact_no=appointment.patient_id).photo_url
        appointment_dict['status'] = appointment.status
        items.append(appointment_dict)

    response_dict["items"] = items

    return response_dict


def doctor_get_allappointment_list(data):
    local_tz = pytz.timezone('Asia/Kolkata')
    doctor = Doctor.objects.get(contact_no=data['doctor_id'])
    appointments_list = doctor.appointment_list.order_by(
        'booked_on')
    response_dict = dict()
    items = []

    for appointment in appointments_list:
        appointment_dict = dict()
        appointment_dict['patient_name'] = Patient.objects.get(contact_no=appointment.patient_id).name
        appointment_dict['patient_age'] = Patient.objects.get(contact_no=appointment.patient_id).age
        appointment_dict['patient_contact'] = Patient.objects.get(contact_no=appointment.patient_id).contact_no
        appointment_dict['patient_photo'] = Patient.objects.get(contact_no=appointment.patient_id).photo_url
        appointment_dict['status'] = appointment.status
        items.append(appointment_dict)

    response_dict["items"] = items

    return response_dict


def terminal_login(data):
    response_dict = dict()
    response_dict['credential_valid'] = False
    if Doctor.objects.filter(contact_no=data['username']).exists():
        if Doctor.objects.get(contact_no=data['username']).doctor_terminal_password == data['password']:
            response_dict['credential_valid'] = True
            response_dict['contact_no'] = data['username']
    return response_dict


def qr_scan(data):
    local_tz = pytz.timezone('Asia/Kolkata')
    current_date = timezone.now().astimezone(local_tz).date()
    response_dict = dict()
    response_dict['valid_qr'] = False
    response_dict['message'] = "Invalid Qr Code"

    abc = Doctor.objects.get(contact_no=data['contact_no']).appointment_list.filter(
        appointment_id=data['appointment_id']).first()
    if Doctor.objects.get(contact_no=data['contact_no']).appointment_list.filter(
            Q(appointment_id=data['appointment_id']) & Q(on_date=current_date) & Q(status='Booked')).exists():
        appointment = Appointments.objects.get(appointment_id=data['appointment_id'])
        response_dict['patient_name'] = Patient.objects.get(contact_no=appointment.patient_id).name
        response_dict['patient_photo'] = Patient.objects.get(contact_no=appointment.patient_id).photo_url
        response_dict['valid_qr'] = True
        if appointment.booking_no == Doctor.objects.get(contact_no=data['contact_no']).current_appointment_no + 1:
            response_dict['message'] = "Go inside"
            doctor = Doctor.objects.get(contact_no=data['contact_no'])
            doctor.current_appointment_no = doctor.current_appointment_no + 1
            doctor.save()
            appointment.status = "done"
            appointment.save()
        else:
            response_dict['message'] = "not your turn"

    return response_dict


def refresh_current_booking_no():
    for doctor in Doctor.objects.all():
        doctor.current_appointment_no = 0
        doctor.save()
