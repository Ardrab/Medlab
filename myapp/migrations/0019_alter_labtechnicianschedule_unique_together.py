# Generated by Django 5.0.6 on 2024-09-04 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_labtechnicianschedule_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='labtechnicianschedule',
            unique_together=set(),
        ),
    ]