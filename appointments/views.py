from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

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
    return render(request, "home.html", context)


class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related("resident", "application")
        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()

        if query:
            queryset = queryset.filter(
                Q(resident__last_name__icontains=query)
                | Q(resident__first_name__icontains=query)
                | Q(application__document_type__icontains=query)
                | Q(application__permit_type__icontains=query)
                | Q(notes__icontains=query)
            )
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Appointment.STATUS_CHOICES
        return context


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointments/appointment_detail.html"
    context_object_name = "appointment"


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = "appointments/appointment_confirm_delete.html"
    success_url = reverse_lazy("appointment_list")
