# Generated by Django 5.2.1 on 2025-05-25 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_tasksubmission_jurnal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksubmission',
            name='task_upload',
            field=models.CharField(choices=[('articles', 'Maqola'), ('certificates', 'AKT sertifikatlar'), ('created', 'Ixtiro')], default='articles'),
        ),
    ]
