# Generated by Django 5.0.7 on 2024-07-25 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0007_alter_ricovero_codospedale_alter_ricovero_paziente'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patologiaricovero',
            options={'managed': False},
        ),
    ]