from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=settings.MEDIA_ROUTE + '\caffeinate.jpg', upload_to=settings.MEDIA_ROUTE + '\\')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        scaled_image = Image.open(self.image.path)
        if scaled_image.height > 100 or scaled_image.width > 100:
            output_size = (100, 100)
            scaled_image.thumbnail(output_size)
            scaled_image.save(self.image.path)


    def get_absolute_url(self):
        return reverse('login')