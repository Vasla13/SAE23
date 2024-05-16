# Generated by Django 5.0.6 on 2024-05-16 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_etudiant', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('groupe', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('coefficient', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('semestre', models.CharField(max_length=10)),
                ('credit_ects', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.FloatField()),
                ('appreciation', models.TextField()),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.etudiant')),
                ('examen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.examen')),
            ],
        ),
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_ressource', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
                ('descriptif', models.TextField()),
                ('coefficient', models.FloatField()),
                ('ue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ue')),
            ],
        ),
    ]
