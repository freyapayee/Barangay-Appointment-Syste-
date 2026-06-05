from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("resident", "application", "appointment_date", "appointment_time", "status")
    list_filter = ("status", "appointment_date")
    search_fields = ("resident__last_name", "resident__first_name", "notes")
