# Generated by Django 4.2.1 on 2023-07-07 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rentsbook_book_alter_rentsbook_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentsbook',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
