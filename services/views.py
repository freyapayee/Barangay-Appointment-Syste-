from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ServiceApplicationForm
from .models import ServiceApplication


class ApplicationListView(ListView):
    model = ServiceApplication
    template_name = "services/application_list.html"
    context_object_name = "applications"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related("resident")
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        status = self.request.GET.get("status", "").strip()

        if query:
            queryset = queryset.filter(
                Q(resident__last_name__icontains=query)
                | Q(resident__first_name__icontains=query)
                | Q(document_type__icontains=query)
                | Q(permit_type__icontains=query)
                | Q(purpose__icontains=query)
            )
        if category:
            queryset = queryset.filter(category=category)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceApplication.CATEGORY_CHOICES
        context["statuses"] = ServiceApplication.STATUS_CHOICES
        return context


class ApplicationDetailView(DetailView):
    model = ServiceApplication
    template_name = "services/application_detail.html"
    context_object_name = "application"


class ApplicationCreateView(CreateView):
    model = ServiceApplication
    form_class = ServiceApplicationForm
    template_name = "services/application_form.html"


class ApplicationUpdateView(UpdateView):
    model = ServiceApplication
    form_class = ServiceApplicationForm
    template_name = "services/application_form.html"


class ApplicationDeleteView(DeleteView):
    model = ServiceApplication
    template_name = "services/application_confirm_delete.html"
    success_url = reverse_lazy("application_list")
