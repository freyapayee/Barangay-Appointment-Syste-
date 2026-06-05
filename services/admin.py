from django.contrib import admin

from .models import ServiceApplication


@admin.register(ServiceApplication)
class ServiceApplicationAdmin(admin.ModelAdmin):
    list_display = ("resident", "category", "service_name", "status", "date_applied")
    list_filter = ("category", "document_type", "permit_type", "status")
    search_fields = (
        "resident__last_name",
        "resident__first_name",
        "resident__address",
        "purpose",
    )
