from django import forms
from django.forms import inlineformset_factory
from .models import Etudiant, UE, Ressource, Enseignant, Examen, Note, RessourceUE, Groupe

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['numero_etudiant','nom', 'prenom', 'groupe', 'photo', 'email']
        
class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['identifiant', 'email']

class UEForm(forms.ModelForm):
    class Meta:
        model = UE
        fields = ['code', 'nom', 'credit_ects']

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['code', 'nom', 'description']
        
RessourceUEFormSet = inlineformset_factory(
    Ressource, RessourceUE, fields=('unite_enseignement', 'coefficient'), extra=1, can_delete=True)

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['numero_professeur','nom', 'prenom', 'email']


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['titre', 'enseignants', 'ressource']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['examen', 'etudiant', 'note', 'appreciation']

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Choisir un fichier CSV')


class ExportDataForm(forms.Form):
    etudiants = forms.ModelMultipleChoiceField(
        queryset=Etudiant.objects.all(), required=False, label='Étudiants', widget=forms.CheckboxSelectMultiple
    )
    ues = forms.ModelMultipleChoiceField(
        queryset=UE.objects.all(), required=False, label='Unités d\'enseignement (UE)', widget=forms.CheckboxSelectMultiple
    )
    ressources = forms.ModelMultipleChoiceField(
        queryset=Ressource.objects.all(), required=False, label='Ressources', widget=forms.CheckboxSelectMultiple
    )
    enseignants = forms.ModelMultipleChoiceField(
        queryset=Enseignant.objects.all(), required=False, label='Enseignants', widget=forms.CheckboxSelectMultiple
    )
    examens = forms.ModelMultipleChoiceField(
        queryset=Examen.objects.all(), required=False, label='Examens', widget=forms.CheckboxSelectMultiple
    )
    notes = forms.ModelMultipleChoiceField(
        queryset=Note.objects.all(), required=False, label='Notes', widget=forms.CheckboxSelectMultiple
    )
    