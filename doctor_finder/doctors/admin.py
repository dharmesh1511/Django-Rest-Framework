# Register your models here.
from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialty', 'phone', 'city')
    search_fields = ('name', 'specialty', 'phone', 'city')
