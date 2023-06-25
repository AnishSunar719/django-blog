from django.db import models

from django.contrib.auth.models import User

from django.utils.text import slugify

from django.core.files.storage import FileSystemStorage

# fs = FileSystemStorage()

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
    
    def delete(self, *args, **kwargs):
        # tell what you need to delete. for image, its path and its storage is essential
        storage, path = self.image.storage, self.image.path
        # Deleting the instance before deleting files related to the instance
        super(Blog, self).delete(*args, **kwargs)
        # Deleting the file
        # storage.delete(path)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)