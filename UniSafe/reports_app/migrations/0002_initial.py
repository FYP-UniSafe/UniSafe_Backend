# Generated by Django 5.0.1 on 2024-03-20 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports_app', '0001_initial'),
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='assigned_gd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users_app.genderdesk'),
        ),
        migrations.AddField(
            model_name='report',
            name='assigned_officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users_app.police'),
        ),
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reported_cases', to='users_app.student'),
        ),
    ]
