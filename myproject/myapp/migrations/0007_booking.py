# Generated by Django 5.0.6 on 2024-08-13 16:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_testtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('appointment_time', models.TimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('scheduled', 'Scheduled')], default='pending', max_length=20)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.testname')),
                ('test_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.testtype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
