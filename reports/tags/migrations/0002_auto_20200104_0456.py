# Generated by Django 2.2.8 on 2020-01-04 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]