from os import path
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from PIL import Image
from resizeimage import resizeimage

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    cite = models.TextField(blank=True)
    cite_author = models.TextField(blank=True)
    interviews = models.TextField(blank=True)
    puplic = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def save(self):
        super().save()
        img = Image.open(self.photo.path)
        if img.width > 690:
            img = resizeimage.resize_cover(img, [690, int((img.height / img.width)*690)])
            img.save(self.photo.path)


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)