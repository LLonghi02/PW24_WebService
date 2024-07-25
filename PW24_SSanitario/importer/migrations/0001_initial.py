# Generated by Django 5.0.7 on 2024-07-23 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cittadino',
            fields=[
                ('CSSN', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50)),
                ('cognome', models.CharField(max_length=50)),
                ('dataNascita', models.DateField(blank=True, null=True)),
                ('luogoNascita', models.CharField(blank=True, max_length=100, null=True)),
                ('indirizzo', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patologia',
            fields=[
                ('cod', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50)),
                ('criticità', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ospedale',
            fields=[
                ('codice', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('città', models.CharField(max_length=100)),
                ('indirizzo', models.CharField(blank=True, max_length=200, null=True)),
                ('direttoreSanitario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='importer.cittadino')),
            ],
        ),
        migrations.CreateModel(
            name='PatologiaCronica',
            fields=[
                ('codPatologia', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='importer.patologia')),
            ],
        ),
        migrations.CreateModel(
            name='PatologiaMortale',
            fields=[
                ('codPatologia', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='importer.patologia')),
            ],
        ),
        migrations.CreateModel(
            name='Ricovero',
            fields=[
                ('cod', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('durata', models.IntegerField()),
                ('motivo', models.TextField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('codOspedale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='importer.ospedale')),
                ('paziente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='importer.cittadino')),
            ],
        ),
        migrations.CreateModel(
            name='PatologiaRicovero',
            fields=[
                ('codOspedale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='importer.ospedale')),
                ('codPatologia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='importer.patologia')),
                ('codRicovero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='importer.ricovero')),
            ],
            options={
                'unique_together': {('codOspedale', 'codRicovero', 'codPatologia')},
            },
        ),
    ]
