# Generated by Django 4.2.1 on 2023-06-03 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_books_img_alter_rentsbook_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='addDate',
            field=models.DateField(auto_now_add=True, default='2023-05-05'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='library',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
