from django.core.files import File
from django.core.management.base import BaseCommand
import os
from U_bank.models import PasswordImage

class Command(BaseCommand):
    help = 'Adds numerically named images (1.jpg to 16.jpg) to the PasswordImage model'

    def handle(self, *args, **kwargs):
        # Directory where the images are stored
        image_dir = 'media/password_images/'

        for i in range(1, 17):  # Loop from 1 to 16
            image_name = f"{i}.jpg"
            image_path = os.path.join(image_dir, image_name)

            try:
                with open(image_path, 'rb') as f:
                    image_file = File(f)
                    PasswordImage.objects.create(name=image_name, image=image_file)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added {image_name}'))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f'File not found: {image_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding {image_name}: {str(e)}'))