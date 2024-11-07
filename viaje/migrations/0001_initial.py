# Generated by Django 5.1.3 on 2024-11-06 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alojamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('capacidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EstadoAlojamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoViaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AlojamientoAsignacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colaborador_id_externo', models.CharField(max_length=255)),
                ('colaborador_nombre', models.CharField(max_length=255)),
                ('fecha_ingreso', models.DateField()),
                ('fecha_salida', models.DateField()),
                ('alojamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='viaje.alojamiento')),
            ],
        ),
        migrations.AddField(
            model_name='alojamiento',
            name='estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alojamientos', to='viaje.estadoalojamiento'),
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_viaje', models.DateField()),
                ('vehiculo_id_externo', models.CharField(max_length=255)),
                ('vehiculo_patente', models.CharField(max_length=50)),
                ('conductor_id_externo', models.CharField(max_length=255)),
                ('conductor_nombre', models.CharField(max_length=255)),
                ('id_estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viajes', to='viaje.estadoviaje')),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion_origen', models.CharField(max_length=255)),
                ('direccion_destino', models.CharField(max_length=255)),
                ('orden_ruta', models.IntegerField()),
                ('viaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rutaviaje', to='viaje.viaje')),
            ],
        ),
        migrations.CreateModel(
            name='ViajeColaborador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colaborador_id_externo', models.CharField(max_length=255)),
                ('colaborador_nombre', models.CharField(max_length=255)),
                ('viaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viajes_colaboradores', to='viaje.viaje')),
            ],
        ),
    ]
