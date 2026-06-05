from django.db import models
from django.urls import reverse

from residents.models import Resident
from services.models import ServiceApplication


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("No Show", "No Show"),
    ]

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="appointments")
    application = models.ForeignKey(
        ServiceApplication,
        on_delete=models.SET_NULL,
        related_name="appointments",
        blank=True,
        null=True,
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["appointment_date", "appointment_time"]

    def __str__(self):
        return f"{self.resident} - {self.appointment_date} {self.appointment_time}"

    def get_absolute_url(self):
        return reverse("appointment_detail", kwargs={"pk": self.pk})
