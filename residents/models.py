from django.db import models
from django.urls import reverse


class Resident(models.Model):
    GENDER_CHOICES = [
        ("Female", "Female"),
        ("Male", "Male"),
        ("Other", "Other"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Widowed", "Widowed"),
        ("Separated", "Separated"),
    ]

    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True)
    age = models.PositiveIntegerField()
    address = models.CharField(
        "Sitio/Purok/Subdivision/Street",
        max_length=255,
    )
    previous_address = models.CharField(max_length=255, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    occupation = models.CharField(max_length=120, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    year_of_residency = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return ", ".join(part for part in parts if part)

    def get_absolute_url(self):
        return reverse("resident_detail", kwargs={"pk": self.pk})
