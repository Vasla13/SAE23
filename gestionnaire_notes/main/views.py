from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Etudiant, UE, Ressource, Enseignant, Examen, Note
from .forms import EtudiantForm, UEForm, RessourceForm, EnseignantForm, ExamenForm, NoteForm, UploadFileForm
import csv
from django import forms


def index(request):
    return render(request, 'main/index.html')

def handle_uploaded_file(f):
    with open('uploaded_file.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            # Traitez le fichier CSV ici
            return HttpResponse('File uploaded successfully')
    else:
        form = UploadFileForm()
    return render(request, 'main/upload.html', {'form': form})

# CRUD views for Etudiant
def etudiant_list(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'main/etudiant_list.html', {'etudiants': etudiants})

def etudiant_detail(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    return render(request, 'main/etudiant_detail.html', {'etudiant': etudiant})

def etudiant_create(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('etudiant_list')
    else:
        form = EtudiantForm()
    return render(request, 'main/etudiant_form.html', {'form': form})

def etudiant_update(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            form.save()
            return redirect('etudiant_list')
    else:
        form = EtudiantForm(instance=etudiant)
    return render(request, 'main/etudiant_form.html', {'form': form})

def etudiant_delete(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        etudiant.delete()
        return redirect('etudiant_list')
    return render(request, 'main/etudiant_confirm_delete.html', {'etudiant': etudiant})

# CRUD views for UE
def ue_list(request):
    ues = UE.objects.all()
    return render(request, 'main/ue_list.html', {'ues': ues})

def ue_detail(request, pk):
    ue = get_object_or_404(UE, pk=pk)
    return render(request, 'main/ue_detail.html', {'ue': ue})

def ue_create(request):
    if request.method == 'POST':
        form = UEForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ue_list')
    else:
        form = UEForm()
    return render(request, 'main/ue_form.html', {'form': form})

def ue_update(request, pk):
    ue = get_object_or_404(UE, pk=pk)
    if request.method == 'POST':
        form = UEForm(request.POST, instance=ue)
        if form.is_valid():
            form.save()
            return redirect('ue_list')
    else:
        form = UEForm(instance=ue)
    return render(request, 'main/ue_form.html', {'form': form})

def ue_delete(request, pk):
    ue = get_object_or_404(UE, pk=pk)
    if request.method == 'POST':
        ue.delete()
        return redirect('ue_list')
    return render(request, 'main/ue_confirm_delete.html', {'ue': ue})

# CRUD views for Ressource
def ressource_list(request):
    ressources = Ressource.objects.all()
    return render(request, 'main/ressource_list.html', {'ressources': ressources})

def ressource_detail(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    return render(request, 'main/ressource_detail.html', {'ressource': ressource})

def ressource_create(request):
    if request.method == 'POST':
        form = RessourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ressource_list')
    else:
        form = RessourceForm()
    return render(request, 'main/ressource_form.html', {'form': form})

def ressource_update(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    if request.method == 'POST':
        form = RessourceForm(request.POST, instance=ressource)
        if form.is_valid():
            form.save()
            return redirect('ressource_list')
    else:
        form = RessourceForm(instance=ressource)
    return render(request, 'main/ressource_form.html', {'form': form})

def ressource_delete(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    if request.method == 'POST':
        ressource.delete()
        return redirect('ressource_list')
    return render(request, 'main/ressource_confirm_delete.html', {'ressource': ressource})

# CRUD views for Enseignant
def enseignant_list(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'main/enseignant_list.html', {'enseignants': enseignants})

def enseignant_detail(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    return render(request, 'main/enseignant_detail.html', {'enseignant': enseignant})

def enseignant_create(request):
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enseignant_list')
    else:
        form = EnseignantForm()
    return render(request, 'main/enseignant_form.html', {'form': form})

def enseignant_update(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        form = EnseignantForm(request.POST, instance=enseignant)
        if form.is_valid():
            form.save()
            return redirect('enseignant_list')
    else:
        form = EnseignantForm(instance=enseignant)
    return render(request, 'main/enseignant_form.html', {'form': form})

def enseignant_delete(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        enseignant.delete()
        return redirect('enseignant_list')
    return render(request, 'main/enseignant_confirm_delete.html', {'enseignant': enseignant})

# CRUD views for Examen
def examen_list(request):
    examens = Examen.objects.all()
    return render(request, 'main/examen_list.html', {'examens': examens})

def examen_detail(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    return render(request, 'main/examen_detail.html', {'examen': examen})

def examen_create(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('examen_list')
    else:
        form = ExamenForm()
    return render(request, 'main/examen_form.html', {'form': form})

def examen_update(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            return redirect('examen_list')
    else:
        form = ExamenForm(instance=examen)
    return render(request, 'main/examen_form.html', {'form': form})

def examen_delete(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        examen.delete()
        return redirect('examen_list')
    return render(request, 'main/examen_confirm_delete.html', {'examen': examen})

# CRUD views for Note
def note_list(request):
    notes = Note.objects.all()
    return render(request, 'main/note_list.html', {'notes': notes})

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'main/note_detail.html', {'note': note})

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'main/note_form.html', {'form': form})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'main/note_form.html', {'form': form})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'main/note_confirm_delete.html', {'note': note})

# Function to generate a simple grade report for a student
def grade_report(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    notes = Note.objects.filter(etudiant=etudiant)
    return render(request, 'main/grade_report.html', {'etudiant': etudiant, 'notes': notes})
