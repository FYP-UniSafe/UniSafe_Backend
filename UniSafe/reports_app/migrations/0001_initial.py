# Generated by Django 5.0.1 on 2024-03-18 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('reporter_full_name', models.CharField(editable=False, max_length=255)),
                ('reporter_gender', models.CharField(max_length=6)),
                ('reporter_college', models.CharField(editable=False, max_length=255)),
                ('reporter_reg_no', models.CharField(editable=False, max_length=255)),
                ('reporter_email', models.EmailField(editable=False, max_length=254)),
                ('reporter_phone', models.CharField(editable=False, max_length=20)),
                ('report_for', models.CharField(choices=[('Self', 'Self'), ('Else', 'Else')], max_length=50)),
                ('victim_email', models.EmailField(max_length=254)),
                ('victim_full_name', models.CharField(max_length=255)),
                ('victim_phone', models.CharField(max_length=20)),
                ('victim_gender', models.CharField(max_length=6)),
                ('victim_reg_no', models.CharField(max_length=255)),
                ('victim_college', models.CharField(max_length=255)),
                ('abuse_type', models.TextField(max_length=20)),
                ('date_and_time', models.DateTimeField()),
                ('location', models.TextField(max_length=20)),
                ('description', models.TextField()),
                ('evidence', models.FileField(blank=True, null=True, upload_to='assets/evidence/')),
                ('perpetrator_fullname', models.TextField(max_length=20)),
                ('perpetrator_gender', models.TextField(max_length=20)),
                ('relationship', models.TextField(max_length=20)),
                ('police_status', models.CharField(default='Unfowarded', max_length=20)),
            ],
        ),
    ]
