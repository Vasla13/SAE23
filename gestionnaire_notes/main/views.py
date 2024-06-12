from django.shortcuts import render, get_object_or_404, redirect
from .models import Etudiant, UE, Ressource, Enseignant, Examen, Note, RessourceUE, Groupe, SAE, SaeUE
from .forms import EtudiantForm, UEForm, RessourceForm, EnseignantForm, ExamenForm, NoteForm, UploadFileForm, RessourceUEFormSet, GroupeForm, SAEForm, SaeUEFormSet
from django.http import HttpResponse
from .forms import ExportDataForm
from xhtml2pdf import pisa
import csv
from django.template.loader import get_template
from io import BytesIO
from django.db.models import Avg, Min, Max
import datetime

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def paginate_notes(notes, notes_per_page=10):
    for i in range(0, len(notes), notes_per_page):
        yield notes[i:i + notes_per_page]

def generate_pdf(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    ues = UE.objects.all()
    notes = Note.objects.filter(etudiant=etudiant)

    ue_data = []
    for ue in ues:
        # Filtrer les examens associés aux ressources de cette UE
        ressources_ue = RessourceUE.objects.filter(unite_enseignement=ue).values_list('ressource', flat=True)
        examens_ue = Examen.objects.filter(ressource__in=ressources_ue)
        ue_notes = notes.filter(examen__in=examens_ue)

        if ue_notes.exists():
            moyenne_etudiant = ue_notes.aggregate(Avg('note'))['note__avg']
            moyenne_groupe = Note.objects.filter(examen__in=examens_ue, etudiant__groupe=etudiant.groupe).aggregate(Avg('note'))['note__avg']
            note_max = ue_notes.aggregate(Max('note'))['note__max']
            note_min = ue_notes.aggregate(Min('note'))['note__min']
            ressources = RessourceUE.objects.filter(unite_enseignement=ue)
            saes = SaeUE.objects.filter(unite_enseignement=ue)

            ue_data.append({
                'nom': ue.nom,
                'code': ue.code,
                'moyenne_etudiant': moyenne_etudiant,
                'moyenne_groupe': moyenne_groupe,
                'note_max': note_max,
                'note_min': note_min,
                'ressources': ressources,
                'saes': saes
            })

    context = {
        'etudiant': etudiant,
        'ues': ue_data,
        'current_date': datetime.datetime.now().strftime('%d/%m/%Y'),
        'current_time': datetime.datetime.now().strftime('%H:%M')
    }

    pdf = render_to_pdf('main/grade_report_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Releve_de_note_{etudiant.nom}_{etudiant.prenom}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return redirect('etudiant_detail', pk=pk)

def index(request):
    return render(request, 'main/index.html')

def import_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            data = list(reader)
            
            etudiants = []
            ues = []
            ressources = []
            enseignants = []
            examens = []
            notes = []
            groupes = []
            ressources_ue = []
            saes = []
            saes_ue = []

            current_category = None
            for row in data:
                if not row:
                    continue
                if row[0] in ['Étudiants', 'Unités d\'enseignement (UE)', 'Ressources', 'Enseignants', 'Examens', 'Notes', 'Groupes', 'RessourcesUE', 'SAE', 'SaeUE']:
                    current_category = row[0]
                else:
                    if current_category == 'Étudiants':
                        etudiants.append(row)
                    elif current_category == 'Unités d\'enseignement (UE)':
                        ues.append(row)
                    elif current_category == 'Ressources':
                        ressources.append(row)
                    elif current_category == 'Enseignants':
                        enseignants.append(row)
                    elif current_category == 'Examens':
                        examens.append(row)
                    elif current_category == 'Notes':
                        notes.append(row)
                    elif current_category == 'Groupes':
                        groupes.append(row)
                    elif current_category == 'RessourcesUE':
                        ressources_ue.append(row)
                    elif current_category == 'SAE':
                        saes.append(row)
                    elif current_category == 'SaeUE':
                        saes_ue.append(row)

            context = {
                'etudiants': etudiants,
                'ues': ues,
                'ressources': ressources,
                'enseignants': enseignants,
                'examens': examens,
                'notes': notes,
                'groupes': groupes,
                'ressources_ue': ressources_ue,
                'saes': saes,
                'saes_ue': saes_ue,
            }
            return render(request, 'main/releve_notes.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'main/import.html', {'form': form})

def export_data(request):
    if request.method == 'POST':
        form = ExportDataForm(request.POST)
        if form.is_valid():
            selected_etudiants = form.cleaned_data['etudiants']
            if selected_etudiants:
                etudiant_name = selected_etudiants[0].nom + " " + selected_etudiants[0].prenom
            else:
                etudiant_name = "etudiants"

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="Releve_de_note_de_{etudiant_name}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Relevé de Notes'])
            writer.writerow([])  # Empty row for spacing

            # Exporting Etudiants
            if 'etudiants' in request.POST:
                etudiants = form.cleaned_data['etudiants']
                writer.writerow(['Étudiants'])
                writer.writerow(['N°étudiant', 'Nom', 'Prénom', 'Groupe', 'Photo', 'Email'])
                for etudiant in etudiants:
                    photo_url = request.build_absolute_uri(etudiant.photo.url) if etudiant.photo else ''
                    writer.writerow([etudiant.numero_etudiant, etudiant.nom, etudiant.prenom, etudiant.groupe.identifiant if etudiant.groupe else '', photo_url, etudiant.email])
                writer.writerow([])  # Empty row for spacing

            # Exporting UEs
            if 'ues' in request.POST:
                ues = form.cleaned_data['ues']
                writer.writerow(['Unités d\'enseignement (UE)'])
                writer.writerow(['Code UE', 'Nom', 'Crédit ECTS'])
                for ue in ues:
                    writer.writerow([ue.code, ue.nom, ue.credit_ects])
                writer.writerow([])  # Empty row for spacing

            # Exporting Ressources
            if 'ressources' in request.POST:
                ressources = form.cleaned_data['ressources']
                writer.writerow(['Ressources'])
                writer.writerow(['Code Ressource', 'Nom', 'Description'])
                for ressource in ressources:
                    writer.writerow([ressource.code, ressource.nom, ressource.description])
                writer.writerow([])  # Empty row for spacing

            # Exporting Enseignants
            if 'enseignants' in request.POST:
                enseignants = form.cleaned_data['enseignants']
                writer.writerow(['Enseignants'])
                writer.writerow(['N°professeur', 'Nom', 'Prénom'])
                for enseignant in enseignants:
                    writer.writerow([enseignant.numero_professeur, enseignant.nom, enseignant.prenom, enseignant.email])
                writer.writerow([])  # Empty row for spacing

            # Exporting Examens
            if 'examens' in request.POST:
                examens = form.cleaned_data['examens']
                writer.writerow(['Examens'])
                writer.writerow(['ID', 'Titre', 'N°professeurs', 'Code Ressource','Date', 'Coefficient'])
                for examen in examens:
                    writer.writerow([examen.id, examen.titre, examen.enseignants.all, examen.ressource.code, examen.date, examen.coefficient])
                writer.writerow([])  # Empty row for spacing

            # Exporting Notes
            if 'notes' in request.POST:
                notes = form.cleaned_data['notes']
                writer.writerow(['Notes'])
                writer.writerow(['Examen', 'Étudiant', 'Note', 'Appréciation'])
                for note in notes:
                    writer.writerow([note.examen.id, note.etudiant.numero_etudiant, note.note, note.appreciation])
                writer.writerow([])  # Empty row for spacing

            # Exporting Groupes
            if 'groupes' in request.POST:
                groupes = form.cleaned_data['groupes']
                writer.writerow(['Groupes'])
                writer.writerow(['Identifiant', 'Email'])
                for groupe in groupes:
                    writer.writerow([groupe.identifiant, groupe.email])
                writer.writerow([])  # Empty row for spacing

            # Exporting RessourceUE
            if 'ressources_ue' in request.POST:
                ressources_ue = form.cleaned_data['ressources_ue']
                writer.writerow(['RessourcesUE'])
                writer.writerow(['Code Ressource', 'Code UE', 'Coefficient'])
                for ressource_ue in ressources_ue:
                    writer.writerow([ressource_ue.ressource.code, ressource_ue.unite_enseignement.code, ressource_ue.coefficient])
                writer.writerow([])  # Empty row for spacing

            # Exporting SAE
            if 'saes' in request.POST:
                saes = form.cleaned_data['saes']
                writer.writerow(['SAE'])
                writer.writerow(['Code', 'Nom', 'Description'])
                for sae in saes:
                    writer.writerow([sae.code, sae.nom, sae.description])
                writer.writerow([])  # Empty row for spacing

            # Exporting SaeUE
            if 'saes_ue' in request.POST:
                saes_ue = form.cleaned_data['saes_ue']
                writer.writerow(['SaeUE'])
                writer.writerow(['SAE', 'UE', 'Coefficient'])
                for sae_ue in saes_ue:
                    writer.writerow([sae_ue.sae.code, sae_ue.unite_enseignement.code, sae_ue.coefficient])
                writer.writerow([])  # Empty row for spacing

            return response

    else:
        form = ExportDataForm()
    return render(request, 'main/export.html', {'form': form})

# CRUD views for Groupe
def groupe_list(request):
    groupes = Groupe.objects.all()
    return render(request, 'main/groupe_list.html', {'groupes': groupes})

def groupe_detail(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    return render(request, 'main/groupe_detail.html', {'groupe': groupe})

def groupe_create(request):
    if request.method == 'POST':
        form = GroupeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groupe_list')
    else:
        form = GroupeForm()
    return render(request, 'main/groupe_form.html', {'form': form})

def groupe_update(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    if request.method == 'POST':
        form = GroupeForm(request.POST, instance=groupe)
        if form.is_valid():
            form.save()
            return redirect('groupe_list')
    else:
        form = GroupeForm(instance=groupe)
    return render(request, 'main/groupe_form.html', {'form': form})

def groupe_delete(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    if request.method == 'POST':
        groupe.delete()
        return redirect('groupe_list')
    return render(request, 'main/groupe_confirm_delete.html', {'groupe': groupe})

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
    return render(request, 'main/etudiant_form.html', {'form': form, 'etudiant': etudiant})

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
    coefficients = RessourceUE.objects.filter(ressource=ressource)
    return render(request, 'main/ressource_detail.html', {'ressource': ressource, 'coefficients': coefficients})

def ressource_create(request):
    if request.method == 'POST':
        form = RessourceForm(request.POST)
        formset = RessourceUEFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            ressource = form.save()
            formset.instance = ressource
            formset.save()
            if 'save_and_add' in request.POST:
                return redirect('ressource_update', pk=ressource.pk)
            return redirect('ressource_detail', pk=ressource.pk)
    else:
        form = RessourceForm()
        formset = RessourceUEFormSet()
    return render(request, 'main/ressource_form.html', {'form': form, 'formset': formset})

def ressource_update(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    if request.method == 'POST':
        form = RessourceForm(request.POST, instance=ressource)
        formset = RessourceUEFormSet(request.POST, instance=ressource)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            if 'save_and_add' in request.POST:
                return redirect('ressource_update', pk=ressource.pk)
            return redirect('ressource_detail', pk=ressource.pk)
    else:
        form = RessourceForm(instance=ressource)
        formset = RessourceUEFormSet(instance=ressource)
    return render(request, 'main/ressource_form.html', {'form': form, 'formset': formset})

def ressource_delete(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    if request.method == 'POST':
        ressource.delete()
        return redirect('ressource_list')
    return render(request, 'main/ressource_confirm_delete.html', {'ressource': ressource})

# CRUD views for SAE
def sae_list(request):
    saes = SAE.objects.all()
    return render(request, 'main/sae_list.html', {'saes': saes})

def sae_detail(request, pk):
    sae = get_object_or_404(SAE, pk=pk)
    coefficients = SaeUE.objects.filter(sae=sae)
    return render(request, 'main/sae_detail.html', {'sae': sae, 'coefficients': coefficients})

def sae_create(request):
    if request.method == 'POST':
        form = SAEForm(request.POST)
        formset = SaeUEFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            sae = form.save()
            formset.instance = sae
            formset.save()
            if 'save_and_add' in request.POST:
                return redirect('sae_update', pk=sae.pk)
            return redirect('sae_detail', pk=sae.pk)
    else:
        form = SAEForm()
        formset = SaeUEFormSet()
    return render(request, 'main/sae_form.html', {'form': form, 'formset': formset})

def sae_update(request, pk):
    sae = get_object_or_404(SAE, pk=pk)
    if request.method == 'POST':
        form = SAEForm(request.POST, instance=sae)
        formset = SaeUEFormSet(request.POST, instance=sae)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            if 'save_and_add' in request.POST:
                return redirect('sae_update', pk=sae.pk)
            return redirect('sae_detail', pk=sae.pk)
    else:
        form = SAEForm(instance=sae)
        formset = SaeUEFormSet(instance=sae)
    return render(request, 'main/sae_form.html', {'form': form, 'formset': formset})

def sae_delete(request, pk):
    sae = get_object_or_404(SAE, pk=pk)
    if request.method == 'POST':
        sae.delete()
        return redirect('sae_list')
    return render(request, 'main/sae_confirm_delete.html', {'sae': sae})

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
