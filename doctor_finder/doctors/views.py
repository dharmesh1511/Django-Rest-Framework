from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Doctor
from .serializers import DoctorSerializer
import io

from twilio.rest import Client
from django.conf import settings


def doctor_list(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return HttpResponse(
        JSONRenderer().render(serializer.data),
        content_type='application/json'
    )

def doctor_detail(request, pk):
    doctor = Doctor.objects.get(id=pk)
    serializer = DoctorSerializer(doctor)
    return HttpResponse(
        JSONRenderer().render(serializer.data),
        content_type='application/json'
    )

@csrf_exempt
def doctor_create(request):
    if request.method == 'POST':
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            doctor = serializer.save()

            # Twilio SMS
            if 'phone' in data:
                message = f"Hello {doctor.name}, your profile has been created successfully!"
                try:
                    send_sms(data['phone'], message)
                except Exception as e:
                    print("Twilio SMS Error:", e)

            return HttpResponse(
                JSONRenderer().render({'msg': 'Doctor Created & SMS Sent'}),
                content_type='application/json'
            )
        return HttpResponse(
            JSONRenderer().render(serializer.errors),
            content_type='application/json'
        )

@csrf_exempt
def doctor_update(request, pk):
    if request.method == 'PUT':
        doctor = Doctor.objects.get(id=pk)
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = DoctorSerializer(doctor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(
                JSONRenderer().render({'msg': 'Doctor Updated'}),
                content_type='application/json'
            )
        return HttpResponse(
            JSONRenderer().render(serializer.errors),
            content_type='application/json'
        )

@csrf_exempt
def doctor_delete(request, pk):
    if request.method == 'DELETE':
        doctor = Doctor.objects.get(id=pk)
        doctor.delete()
        return HttpResponse(
            JSONRenderer().render({'msg': 'Doctor Deleted'}),
            content_type='application/json'
        )


from twilio.rest import Client
from django.conf import settings

def send_sms(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_number
    )