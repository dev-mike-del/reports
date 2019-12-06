# Generated by Django 2.2.7 on 2019-12-05 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_admin', '0004_auto_20191205_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicreport',
            name='body',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='body_peer_review',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='body_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='conclusion',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='conclusion_peer_review',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='conclusion_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='executive_summary',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='executive_summary_peer_review',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='executive_summary_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='introduction',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='introduction_peer_review',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='introduction_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='recommendations',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='recommendations_peer_review',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='recommendations_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='references',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='references_peer_review',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='references_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='tags_as_string',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='tags_peer_review',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='tags_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='title_peer_review',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='basicreport',
            name='title_peer_review_response',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
    ]
