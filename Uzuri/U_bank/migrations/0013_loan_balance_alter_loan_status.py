# Generated by Django 5.0.4 on 2025-01-29 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('U_bank', '0012_remove_client_password_image_client_password_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='Balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='loan',
            name='Status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
