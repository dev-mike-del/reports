# Generated by Django 2.2.7 on 2019-12-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_admin', '0010_auto_20191218_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicreport',
            name='id_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='id_year',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
