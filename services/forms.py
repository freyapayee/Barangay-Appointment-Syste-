from django import forms

from .models import ServiceApplication


class ServiceApplicationForm(forms.ModelForm):
    class Meta:
        model = ServiceApplication
        fields = [
            "resident",
            "category",
            "document_type",
            "permit_type",
            "purpose",
            "status",
        ]
        widgets = {
            "purpose": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        document_type = cleaned_data.get("document_type")
        permit_type = cleaned_data.get("permit_type")

        if category == "Document" and not document_type:
            self.add_error("document_type", "Choose a barangay document.")
        if category == "Permit" and not permit_type:
            self.add_error("permit_type", "Choose a permit type.")
        if category != "Document":
            cleaned_data["document_type"] = ""
        if category != "Permit":
            cleaned_data["permit_type"] = ""
        return cleaned_data
