# Generated by Django 2.0.3 on 2018-04-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Content', '0004_doctor_photo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='photo_url',
            field=models.TextField(blank=True),
        ),
    ]