# Generated by Django 5.0.4 on 2024-05-23 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_enseignant_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='SAE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='enseignant',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.CreateModel(
            name='SaeUE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sae')),
                ('unite_enseignement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ue')),
            ],
            options={
                'unique_together': {('sae', 'unite_enseignement')},
            },
        ),
    ]
