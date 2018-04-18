from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from Content.patient_doctor import *


@api_view(['GET', 'POST'])
def add_patient_api(request):
    response_dict = dict()
    try:
        a = request.data
        add_patient(request.data)
        response_dict['user_added'] = True
        return Response(response_dict, status=HTTP_202_ACCEPTED)
    except:
        response_dict['user_added'] = False
        return Response(response_dict, status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def update_patient_api(request):
    update_patient(request.data['userdata'], request.data['patient_id'])
    return Response('user added', status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def add_doctor_api(request):
    a = request.data
    add_doctor(a)
    return Response('user added', status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def update_doctor_api(request):
    update_doctor(request.data['userdata'], request.data['doctor_id'])
    return Response('user added', status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def login2(request):
    try:
        response_dict = dict()
        a = request.data
        # #otp = random.randint(11111, 99999)
        # otp = 12345
        # numbers = []
        # numbers.append(a['contact_no'])
        # client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #     to="+917830969677",
        #     from_="+919838598004",
        #     body="--"+str(otp))

        response_dict['new_user'] = True
        # response_dict['otp'] = otp
        if Patient.objects.filter(contact_no=a['contact_no']).exists():
            response_dict['new_user'] = False
            response_dict['type_doctor'] = True
            patient_detail_dict = dict()
            patient_detail_dict['name'] = Patient.objects.get(contact_no=a['contact_no']).name
            patient_detail_dict['age'] = Patient.objects.get(contact_no=a['contact_no']).age
            patient_detail_dict['contact_no'] = Patient.objects.get(contact_no=a['contact_no']).contact_no
            patient_detail_dict['email_id'] = Patient.objects.get(contact_no=a['contact_no']).email_id
            response_dict['patient_details'] = patient_detail_dict
        if Doctor.objects.filter(contact_no=a['contact_no']).exists():
            response_dict['new_user'] = False
            response_dict['type_doctor'] = False
        return Response(response_dict, status=HTTP_202_ACCEPTED)
    except Exception as e:
        print(e)
        return Response("ok", status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def login(request):
    response_dict = dict()
    response_dict['exist'] = False
    a = request.data
    if Patient.objects.filter(contact_no=a['contact_no']).exists():
        response_dict['exist'] = True
        response_dict['type'] = 'patient'
    if Doctor.objects.filter(contact_no=a['contact_no']).exists():
        response_dict['exist'] = True
        response_dict['type'] = 'doctor'

    if not response_dict['exist']:
        return Response(response_dict, status=HTTP_202_ACCEPTED)

    else:
        if response_dict['type'] == 'doctor':
            return Response(response_dict, status=HTTP_202_ACCEPTED)
        else:
            return Response(response_dict, status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def get_my_appointments(request):
    return Response(get_appointments(request.data['user_id']), status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def get_doctor_list(request):
    return Response(get_filtered_doctor_list(request.data['query']), status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def book_appointment_api(request):
    book_appointments(request.data)
    return Response({"booking_status": True}, status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def login_doctor(request):
    response_dict = dict()
    response_dict['exists'] = False
    if Doctor.objects.filter(email_id=request.data['username']).exists():
        if Doctor.objects.get(email_id=request.data['username']).doctor_terminal_password == request.data['password']:
            response_dict['exists'] = True
            response_dict['contact_no'] = Doctor.objects.get(email_id=request.data['username']).contact_no
    return Response(response_dict, status=HTTP_200_OK)


@api_view(['GET', 'POST'])
def cancel_appointment(request):
    if Appointments.objects.filter(appointment_id="99b99ddb-a5df-40c5-9b4f-f33753b29409").exists():
        appointment = Appointments.objects.get(appointment_id=request.data['appointment_id'])
        patientId = appointment.patient_id
        doctorId = appointment.doctor_id
        doctor = Doctor.objects.get(contact_no=doctorId)
        doctor.appointment_list.remove(appointment)
        doctor.save()
        patient = Patient.objects.get(contact_no=patientId)
        patient.appointment_list.remove(appointment)
        patient.save()
        for appointment_x in Appointments.objects.filter(Q(doctor_id=doctorId) & Q(booking_no__gt=appointment.booking_no) ):
            appointment_x.booking_no = appointment_x.booking_no-1
            appointment_x.save()

    return Response({"cancel_status": True}, status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def doctor_get_appointment(request):
    return Response(doctor_get_todayappointment_list(request.data), status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def terminal_login_api(request):
    return Response(terminal_login(request.data), status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def scanqr(request):
    return Response(qr_scan(request.data), status=HTTP_202_ACCEPTED)
