# Generated by Django 2.2.7 on 2019-12-05 17:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('report_admin', '0002_auto_20191205_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicreport',
            name='eb_slug',
            field=models.SlugField(default=uuid.uuid4, max_length=255, unique=True),
        ),
    ]