from django import forms

from .models import ServiceApplication


class ServiceApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = self.data.get("category") or getattr(self.instance, "category", "")

        self.fields["category"].widget.attrs.update({"data-service-category": "true"})
        self.fields["document_type"].widget.attrs.update({"data-document-type": "true"})
        self.fields["permit_type"].widget.attrs.update({"data-permit-type": "true"})

        if category != "Document":
            self.fields["document_type"].widget.attrs["disabled"] = "disabled"
        if category != "Permit":
            self.fields["permit_type"].widget.attrs["disabled"] = "disabled"

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
