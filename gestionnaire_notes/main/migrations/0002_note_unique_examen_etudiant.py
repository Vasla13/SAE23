# Generated by Django 5.0.4 on 2024-05-22 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='note',
            constraint=models.UniqueConstraint(fields=('examen', 'etudiant'), name='unique_examen_etudiant'),
        ),
    ]
