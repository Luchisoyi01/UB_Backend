# Generated by Django 5.0.4 on 2025-01-09 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('U_bank', '0004_alter_client_password_image_alter_passwordimage_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='Password_Image',
        ),
        migrations.AddField(
            model_name='client',
            name='Password_Image',
            field=models.FileField(blank=True, null=True, upload_to='password_images/'),
        ),
    ]
