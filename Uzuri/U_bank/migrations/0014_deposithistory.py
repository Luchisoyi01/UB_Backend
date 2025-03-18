# Generated by Django 5.0.4 on 2025-02-12 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('U_bank', '0013_loan_balance_alter_loan_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('fixed', 'Fixed Account'), ('salary', 'Salary Account'), ('savings', 'Savings Account')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to='U_bank.client')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
