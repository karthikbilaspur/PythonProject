# complaints/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm
from .models import Complaint

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('view_complaints')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/submit_complaint.html', {'form': form})

@login_required
def view_complaints(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complaints/view_complaints.html', {'complaints': complaints})

@login_required
def update_complaint(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('view_complaints')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'complaints/update_complaint.html', {'form': form})