from django.db import models

# Create your models here.
from django.utils.text import slugify

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField()
    image = models.ImageField(upload_to="artists/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # body = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    description = models.CharField()
    # body = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class Art(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='arts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='arts')
    name = models.TextField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="arts/")
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

