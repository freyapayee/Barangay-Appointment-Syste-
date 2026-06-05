from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ResidentForm
from .models import Resident


class ResidentListView(ListView):
    model = Resident
    template_name = "residents/resident_list.html"
    context_object_name = "residents"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(last_name__icontains=query)
                | Q(first_name__icontains=query)
                | Q(middle_name__icontains=query)
                | Q(address__icontains=query)
            )
        return queryset


class ResidentDetailView(DetailView):
    model = Resident
    template_name = "residents/resident_detail.html"
    context_object_name = "resident"


class ResidentCreateView(CreateView):
    model = Resident
    form_class = ResidentForm
    template_name = "residents/resident_form.html"


class ResidentUpdateView(UpdateView):
    model = Resident
    form_class = ResidentForm
    template_name = "residents/resident_form.html"


class ResidentDeleteView(DeleteView):
    model = Resident
    template_name = "residents/resident_confirm_delete.html"
    success_url = reverse_lazy("resident_list")
