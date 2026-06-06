from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ResidentForm
from .models import Resident


def resident_list(request):
    residents = Resident.objects.all()
    search = request.GET.get("q", "").strip()

    if search:
        residents = residents.filter(
            Q(last_name__icontains=search)
            | Q(first_name__icontains=search)
            | Q(middle_name__icontains=search)
            | Q(address__icontains=search)
        )

    return render(request, "residents/resident_list.html", {"residents": residents})


def resident_detail(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    return render(request, "residents/resident_detail.html", {"resident": resident})


def resident_add(request):
    form = ResidentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("resident_list")

    return render(request, "residents/resident_form.html", {"form": form})


def resident_edit(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    form = ResidentForm(request.POST or None, instance=resident)
    if form.is_valid():
        form.save()
        return redirect("resident_detail", pk=resident.pk)

    return render(request, "residents/resident_form.html", {"form": form, "object": resident})


def resident_delete(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    if request.method == "POST":
        resident.delete()
        return redirect("resident_list")

    return render(request, "residents/resident_confirm_delete.html", {"object": resident})
