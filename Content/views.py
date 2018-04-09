from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from twilio.rest import Client
from Content.patient_doctor import *


account_sid = 'AC899d7d4b951dd4ecaf2c87884b16596d'

auth_token = '3a6173b29a12f22a9e066d9166c471c4'

@api_view(['GET', 'POST'])
def add_patient_api(request):
    add_patient(request.data)
    return Response('user added', status=HTTP_202_ACCEPTED)


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
        #otp = random.randint(11111, 99999)
        otp = 12345
        numbers = []
        numbers.append(a['contact_no'])
        client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #     to="+917830969677",
        #     from_="+919838598004",
        #     body="--"+str(otp))

        response_dict['new_user'] = True
        response_dict['otp'] = otp
        if Patient.objects.filter(contact_no=a['contact_no']).exists():
            response_dict['new_user'] = False
            response_dict['type'] = 'patient'
        if Doctor.objects.filter(contact_no=a['contact_no']).exists():
            response_dict['new_user'] = True
            response_dict['type'] = 'doctor'

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
    return Response('Booked', status=HTTP_202_ACCEPTED)
