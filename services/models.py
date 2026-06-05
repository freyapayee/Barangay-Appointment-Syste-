from django.db import models
from django.urls import reverse

from residents.models import Resident


class ServiceApplication(models.Model):
    CATEGORY_CHOICES = [
        ("Document", "Barangay Certificate"),
        ("Registration", "Barangay Registration"),
        ("Permit", "Permit"),
    ]

    DOCUMENT_CHOICES = [
        ("Indigency", "Indigency"),
        ("Residency", "Residency"),
        ("Clearance", "Clearance"),
    ]

    PERMIT_CHOICES = [
        ("Building", "Building"),
        ("Business", "Business"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Approved", "Approved"),
        ("Released", "Released"),
        ("Rejected", "Rejected"),
    ]

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="applications")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_CHOICES, blank=True)
    permit_type = models.CharField(max_length=20, choices=PERMIT_CHOICES, blank=True)
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    date_applied = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_applied", "-updated_at"]

    def __str__(self):
        return f"{self.resident} - {self.service_name}"

    @property
    def service_name(self):
        if self.category == "Document":
            return self.document_type or "Barangay Certificate"
        if self.category == "Permit":
            return f"{self.permit_type} Permit" if self.permit_type else "Permit"
        return "Barangay Registration"

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk})
