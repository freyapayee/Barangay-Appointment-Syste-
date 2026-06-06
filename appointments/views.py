from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from residents.models import Resident
from services.models import ServiceApplication

from .forms import AppointmentForm
from .models import Appointment


def home(request):
    service_counts = {
        item["category"]: item["total"]
        for item in ServiceApplication.objects.values("category").annotate(total=Count("id"))
    }
    context = {
        "resident_count": Resident.objects.count(),
        "appointment_count": Appointment.objects.count(),
        "document_count": service_counts.get("Document", 0),
        "registration_count": service_counts.get("Registration", 0),
        "permit_count": service_counts.get("Permit", 0),
        "recent_residents": Resident.objects.order_by("-created_at")[:5],
        "recent_applications": ServiceApplication.objects.select_related("resident")[:5],
        "upcoming_appointments": Appointment.objects.select_related("resident", "application")[:5],
    }
    return render(request, "appointments/home.html", context)


def appointment_list(request):
    appointments = Appointment.objects.select_related("resident", "application")
    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    if search:
        appointments = appointments.filter(
            Q(resident__last_name__icontains=search)
            | Q(resident__first_name__icontains=search)
            | Q(application__document_type__icontains=search)
            | Q(application__permit_type__icontains=search)
            | Q(notes__icontains=search)
        )
    if status:
        appointments = appointments.filter(status=status)

    context = {
        "appointments": appointments,
        "statuses": Appointment.STATUS_CHOICES,
    }
    return render(request, "appointments/appointment_list.html", context)


def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, "appointments/appointment_detail.html", {"appointment": appointment})


def appointment_add(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("appointment_list")

    return render(request, "appointments/appointment_form.html", {"form": form})


def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        return redirect("appointment_detail", pk=appointment.pk)

    return render(request, "appointments/appointment_form.html", {"form": form, "object": appointment})


def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect("appointment_list")

    return render(request, "appointments/appointment_confirm_delete.html", {"object": appointment})
