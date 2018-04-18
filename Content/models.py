from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class Appointments(models.Model):
    appointment_id = models.TextField(unique=True)
    patient_id = models.TextField()
    doctor_id = models.TextField()
    booked_on = models.DateTimeField()
    on_date = models.DateField()
    estimated_time = models.DateTimeField(null=True, blank=True)
    fees_paid = models.BooleanField()
    status = models.TextField()
    booking_no = models.IntegerField(null=True, blank=True)


class Patient(models.Model):
    name = models.TextField()
    age = models.IntegerField()
    email_id = models.EmailField(unique=True)
    appointment_list = models.ManyToManyField(Appointments, blank=True)
    contact_no = models.TextField(unique=True)
    photo_url = models.TextField(blank=True)


class Doctor(models.Model):
    name = models.TextField()
    speciality = models.TextField()
    fees = models.IntegerField()
    appointment_list = models.ManyToManyField(Appointments, blank=True)
    contact_no = models.TextField(unique=True)
    email_id = models.EmailField(unique=True)
    experience = models.IntegerField()
    age = models.IntegerField()
    degree = models.TextField(null=True)
    doctor_terminal_login = models.TextField()
    doctor_terminal_password = models.TextField()
    independent_doctor = models.BooleanField()
    address = models.TextField()
    photo_url = models.TextField(blank=True)
    current_appointment_no = models.IntegerField(blank=True,null=True)
