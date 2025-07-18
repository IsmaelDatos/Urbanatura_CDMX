# Generated by Django 4.2.11 on 2025-06-29 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudTraslado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.DecimalField(decimal_places=6, default=19.4326, max_digits=9)),
                ('longitud', models.DecimalField(decimal_places=6, default=-99.1332, max_digits=9)),
                ('motivo_traslado', models.CharField(choices=[('conservacion', 'Conservación del árbol'), ('construccion', 'Obra de construcción'), ('mejor_ubicacion', 'Mejor ubicación para su desarrollo'), ('riesgo', 'Por riesgo en ubicación actual')], max_length=20)),
                ('foto_traslado', models.ImageField(upload_to='traslado/')),
                ('ubicacion_actual_traslado', models.CharField(choices=[('banqueta', 'Banqueta'), ('camellon', 'Camellón'), ('jardin_privado', 'Jardín privado'), ('area_verde', 'Área verde pública')], max_length=20)),
                ('calle_actual_traslado', models.CharField(max_length=100)),
                ('numero_ext_actual_traslado', models.CharField(max_length=10)),
                ('numero_int_actual_traslado', models.CharField(blank=True, max_length=10, null=True)),
                ('alcaldia_actual_traslado', models.CharField(max_length=50)),
                ('colonia_actual_traslado', models.CharField(max_length=50)),
                ('cp_actual_traslado', models.CharField(max_length=5)),
                ('calle_nueva_traslado', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_ext_nueva_traslado', models.CharField(blank=True, max_length=10, null=True)),
                ('alcaldia_nueva_traslado', models.CharField(blank=True, max_length=50, null=True)),
                ('colonia_nueva_traslado', models.CharField(blank=True, max_length=50, null=True)),
                ('info_adicional_traslado', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('requiere_inspeccion', 'Requiere inspección')], default='pendiente', max_length=20)),
            ],
            options={
                'verbose_name': 'Solicitud de Traslado',
                'verbose_name_plural': 'Solicitudes de Traslado',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
