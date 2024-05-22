from django.db import models

class Groupe(models.Model):
    identifiant = models.CharField(max_length=4)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.identifiant}'
    
class Etudiant(models.Model):
    numero_etudiant = models.CharField(max_length=8)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f'{self.nom} {self.prenom}'

class UE(models.Model):
    code = models.CharField(max_length=16)
    nom = models.CharField(max_length=100)
    credit_ects = models.IntegerField()

    def __str__(self):
        return self.code

class Ressource(models.Model):
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.nom}"
    
class RessourceUE(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    unite_enseignement = models.ForeignKey(UE, on_delete=models.CASCADE)
    coefficient = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('ressource', 'unite_enseignement')

class Enseignant(models.Model):
    numero_professeur = models.CharField(max_length=8)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f'{self.nom} {self.prenom}'

class Examen(models.Model):
    titre = models.CharField(max_length=100)
    enseignants = models.ManyToManyField(Enseignant, related_name='examens')
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True, blank=True)
    coefficient = models.FloatField(default='1.0')

    def __str__(self):
        noms_enseignants = "_".join([enseignant.nom for enseignant in self.enseignants.all()])
        return f"{self.titre}_{noms_enseignants}"

class Note(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    note = models.FloatField()
    appreciation = models.TextField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['examen', 'etudiant'], name='unique_examen_etudiant')
        ]

    def __str__(self):
        return f"{self.examen} - {self.etudiant.nom}"

