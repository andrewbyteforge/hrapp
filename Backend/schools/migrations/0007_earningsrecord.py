# Generated by Django 5.0 on 2023-12-30 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0006_employee_schools'),
    ]

    operations = [
        migrations.CreateModel(
            name='EarningsRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_year', models.CharField(max_length=20)),
                ('total_earned', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employ_earned', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ed5_earned', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.employee')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.school')),
            ],
        ),
    ]
