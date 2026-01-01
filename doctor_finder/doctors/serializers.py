from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    specialty = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=15)
    city = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Doctor.objects.create(**validated_data)
    
    def validate_phone(self, value):
        if self.instance:  # update case
            return value
        if Doctor.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Doctor with this phone already exists!")
        return value

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.specialty = validated_data.get('specialty', instance.specialty)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance

