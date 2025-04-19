# Generated by Django 5.2 on 2025-04-19 19:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudDerribo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo_derribo', models.CharField(choices=[('riesgo', 'Riesgo de caída'), ('enfermedad', 'Enfermedad irreversible'), ('construccion', 'Para construcción'), ('obstruccion', 'Obstrucción grave'), ('otro', 'Otro motivo')], max_length=20)),
                ('foto_derribo', models.ImageField(upload_to='derribo/')),
                ('ubicacion_derribo', models.CharField(choices=[('banqueta', 'Banqueta'), ('camellon', 'Camellón'), ('propiedad_privada', 'Propiedad privada'), ('area_publica', 'Área pública')], max_length=20)),
                ('calle_derribo', models.CharField(max_length=100)),
                ('numero_ext_derribo', models.CharField(max_length=10)),
                ('numero_int_derribo', models.CharField(blank=True, max_length=10, null=True)),
                ('alcaldia_derribo', models.CharField(max_length=50)),
                ('colonia_derribo', models.CharField(max_length=50)),
                ('cp_derribo', models.CharField(max_length=5)),
                ('justificacion_derribo', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('requiere_aprobacion', 'Requiere aprobación especial')], default='pendiente', max_length=20)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_derribo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Solicitud de Derribo',
                'verbose_name_plural': 'Solicitudes de Derribo',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
