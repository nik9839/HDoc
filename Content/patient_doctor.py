import pytz
from django.db.models import Q
from Content.models import Patient, Doctor, Appointments
import string
import random, uuid
from django.utils import timezone
import dateutil.parser


def add_patient(data):
    patient_obj = Patient(name=data['name'], age=data['age'], email_id=data['email_id'],
                          contact_no=data['contact_no'])
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
    doctor_obj = Doctor(name=data['name'], fees=data['fees'], email_id=data['email_id'],
                        contact_no=data['contact_no'], speciality=data['speciality'], age=data['age'],
                        experience=data['experience'], degree=data['degree'], doctor_terminal_login=id_generator(6),
                        doctor_terminal_password=str(id_generator(8, string.digits)),
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
    appointments_list = Appointments.objects.filter(patient_id=p_id).order_by('on_date')

    appointments_dict = dict()
    items = []
    for appointment in appointments_list:
        appointment_dict = dict()
        appointment_dict['doctor_name'] = Doctor.objects.get(contact_no=appointment.doctor_id).name
        appointment_dict['doctor_address'] = Doctor.objects.get(contact_no=appointment.doctor_id).address
        appointment_dict['status'] = appointment.status
        appointment_dict['on_date'] = appointment.on_date
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

        items.append(doctor_dict)

    doctors_dict['items'] = items
    return doctors_dict


def book_appointments(data):
    d_id = data['d_id']
    p_id = data['p_id']
    local_tz = pytz.timezone('Asia/Kolkata')
    appointment_date = dateutil.parser.parse(data['appointment_date']).astimezone(local_tz).date()
    current_dateTime = timezone.now().astimezone(local_tz)

    appointment = Appointments(appointment_id=uuid.uuid4(), patient_id=p_id, doctor_id=d_id, status='booked',
                               on_date=appointment_date, fees_paid=data['fees_paid'], booked_on=current_dateTime)

    appointment.save()

    patient = Patient.objects.get(contact_no=p_id)
    patient.appointment_list.add(appointment)
    patient.save()
    doctor = Doctor.objects.get(contact_no=d_id)
    doctor.appointment_list.add(appointment)
    doctor.save()
