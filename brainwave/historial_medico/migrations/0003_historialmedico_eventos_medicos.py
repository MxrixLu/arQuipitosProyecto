# Generated by Django 5.2 on 2025-05-04 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos_medicos', '0001_initial'),
        ('historial_medico', '0002_alter_historialmedico_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialmedico',
            name='eventos_medicos',
            field=models.ManyToManyField(related_name='historiales', to='eventos_medicos.examen'),
        ),
    ]
