from django import forms
from django.forms import inlineformset_factory
from .models import Etudiant, UE, Ressource, Enseignant, Examen, Note, RessourceUE, Groupe, SAE, SaeUE

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

class SAEForm(forms.ModelForm):
    class Meta:
        model = SAE
        fields = ['code', 'nom', 'description']
        
SaeUEFormSet = inlineformset_factory(
    SAE, SaeUE, fields=('unite_enseignement', 'coefficient'), extra=1, can_delete=True)

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
        queryset=Etudiant.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ues = forms.ModelMultipleChoiceField(
        queryset=UE.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ressources = forms.ModelMultipleChoiceField(
        queryset=Ressource.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    enseignants = forms.ModelMultipleChoiceField(
        queryset=Enseignant.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    examens = forms.ModelMultipleChoiceField(
        queryset=Examen.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    notes = forms.ModelMultipleChoiceField(
        queryset=Note.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    groupes = forms.ModelMultipleChoiceField(
        queryset=Groupe.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ressources_ue = forms.ModelMultipleChoiceField(
        queryset=RessourceUE.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    saes = forms.ModelMultipleChoiceField(
        queryset=SAE.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    sae_ue = forms.ModelMultipleChoiceField(
        queryset=SaeUE.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    