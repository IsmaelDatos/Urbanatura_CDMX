# Generated by Django 4.2.11 on 2025-06-30 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trasplante', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='alcaldia_actual_traslado',
            field=models.CharField(max_length=60, verbose_name='Alcaldía actual'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='alcaldia_nueva_traslado',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Alcaldía nueva'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='calle_actual_traslado',
            field=models.CharField(max_length=120, verbose_name='Calle actual'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='calle_nueva_traslado',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Calle nueva'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='colonia_actual_traslado',
            field=models.CharField(max_length=120, verbose_name='Colonia actual'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='colonia_nueva_traslado',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Colonia nueva'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='cp_actual_traslado',
            field=models.CharField(max_length=5, verbose_name='Código postal actual'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='foto_traslado',
            field=models.TextField(verbose_name='Imagen del árbol en Base64'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='info_adicional_traslado',
            field=models.TextField(verbose_name='Información adicional'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='latitud',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='longitud',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='numero_ext_actual_traslado',
            field=models.CharField(max_length=10, verbose_name='Número exterior actual'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='numero_ext_nueva_traslado',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Número exterior nuevo'),
        ),
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='numero_int_actual_traslado',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Número interior actual'),
        ),
    ]
