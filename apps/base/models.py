from django.db import models
from django.db.models.signals import pre_delete

from django.contrib.auth.models import User

from django.utils.text import slugify

from django.core.files.storage import FileSystemStorage

from django.dispatch import receiver

import os

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, unique=True, blank=True)
    image = models.ImageField(upload_to='blog')
    description = models.TextField(blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f'{self.title} -----> {self.description[:15]}...'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

# Making method that does the deleting of images when instance is deleted
@receiver(signal=pre_delete, sender=Blog)
def delete_image(sender, instance, **kwargs):
    file_path = instance.image.path
    if os.path.isfile(file_path):
        os.remove(file_path)
    
# Registering signal with model
pre_delete.connect(delete_image, sender=Blog)