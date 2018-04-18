from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Content import views

urlpatterns = [
    path('addpatient', views.add_patient_api),
    path('updatepatient', views.update_patient_api),
    path('adddoctor', views.add_doctor_api),
    path('updatedoctor', views.update_doctor_api),
    path('login', views.login2),
    path('myappointments', views.get_my_appointments),
    path('getdoctorlist', views.get_doctor_list),
    path('bookappointment', views.book_appointment_api),
    path('doctorlogin', views.login_doctor),
    path('cancelappointment',views.cancel_appointment),
    path('doctorappointments',views.cancel_appointment),
    path('terminallogin',views.terminal_login_api),
    path('qrscan',views.scanqr)

]

urlpatterns = format_suffix_patterns(urlpatterns)
