from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ServiceApplicationForm
from .models import ServiceApplication


def application_list(request):
    applications = ServiceApplication.objects.select_related("resident")
    search = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    if search:
        applications = applications.filter(
            Q(resident__last_name__icontains=search)
            | Q(resident__first_name__icontains=search)
            | Q(document_type__icontains=search)
            | Q(permit_type__icontains=search)
            | Q(purpose__icontains=search)
        )
    if category:
        applications = applications.filter(category=category)
    if status:
        applications = applications.filter(status=status)

    context = {
        "applications": applications,
        "categories": ServiceApplication.CATEGORY_CHOICES,
        "statuses": ServiceApplication.STATUS_CHOICES,
    }
    return render(request, "services/application_list.html", context)


def application_detail(request, pk):
    application = get_object_or_404(ServiceApplication, pk=pk)
    return render(request, "services/application_detail.html", {"application": application})


def application_add(request):
    form = ServiceApplicationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("application_list")

    return render(request, "services/application_form.html", {"form": form})


def application_edit(request, pk):
    application = get_object_or_404(ServiceApplication, pk=pk)
    form = ServiceApplicationForm(request.POST or None, instance=application)
    if form.is_valid():
        form.save()
        return redirect("application_detail", pk=application.pk)

    return render(request, "services/application_form.html", {"form": form, "object": application})


def application_delete(request, pk):
    application = get_object_or_404(ServiceApplication, pk=pk)
    if request.method == "POST":
        application.delete()
        return redirect("application_list")

    return render(request, "services/application_confirm_delete.html", {"object": application})
