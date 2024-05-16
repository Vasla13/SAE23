from django.db import models

class Etudiant(models.Model):
    numero_etudiant = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    groupe = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f'{self.nom} {self.prenom}'

class UE(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    semestre = models.CharField(max_length=10)
    credit_ects = models.IntegerField()

    def __str__(self):
        return self.nom

class Ressource(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    code_ressource = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    descriptif = models.TextField()
    coefficient = models.FloatField()

    def __str__(self):
        return self.nom

class Enseignant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nom} {self.prenom}'

class Examen(models.Model):
    titre = models.CharField(max_length=100)
    date = models.DateField()
    coefficient = models.FloatField()

    def __str__(self):
        return self.titre

class Note(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    note = models.FloatField()
    appreciation = models.TextField()

    def __str__(self):
        return f'{self.etudiant} - {self.examen}'
