from django.contrib import admin

from .models import Resident


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age", "gender", "address", "year_of_residency")
    list_filter = ("gender", "marital_status")
    search_fields = ("last_name", "first_name", "middle_name", "address")
