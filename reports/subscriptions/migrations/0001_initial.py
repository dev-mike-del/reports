# Generated by Django 2.2.8 on 2020-01-04 01:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('subscriber_slug', models.SlugField(default=uuid.uuid4, max_length=255, unique=True)),
                ('tags', models.ManyToManyField(blank=True, to='tags.Tag')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriber_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
