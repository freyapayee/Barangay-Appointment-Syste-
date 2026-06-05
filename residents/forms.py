from django import forms

from .models import Resident


class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = [
            "last_name",
            "first_name",
            "middle_name",
            "age",
            "address",
            "previous_address",
            "marital_status",
            "occupation",
            "gender",
            "year_of_residency",
        ]
        widgets = {
            "address": forms.TextInput(attrs={"placeholder": "Sitio/Purok/Subdivision/Street"}),
            "previous_address": forms.TextInput(attrs={"placeholder": "Previous address"}),
        }
