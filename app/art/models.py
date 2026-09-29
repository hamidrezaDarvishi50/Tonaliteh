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

class Tag(models.Model):

    class TagType(models.TextChoices):
        DOMINANT_COLOR = "dominant_color", "Dominant Color"
        SUBJECT = "subject", "Subject"
        OBJECT = "object", "Object"
        ACTION = "action", "Action"
        STYLE = "style", "Style"

    type = models.CharField(max_length=30, choices=TagType.choices)
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["type", "name"], name="unique_tag_type_name")]

class Art(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='arts')
    category = models.ManyToManyField(Category, related_name='arts', blank=False)
    tags = models.ManyToManyField(Tag, related_name="arts", blank=True)
    
    artist_order = models.IntegerField(default=0)
    category_order = models.IntegerField(default=0)
    display_order = models.IntegerField(default=0)
    
    name = models.TextField(max_length=255)
    persian_name = models.TextField(max_length=255, default="")
    slug = models.SlugField(unique=True, blank=True)
    
    image = models.ImageField(upload_to="arts/")
    voice = models.FileField(upload_to="arts/voices/", blank=True, null=True)
    second_voice = models.FileField(upload_to="arts/voices/", blank=True, null=True)
    
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    released_year = models.PositiveIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Frame(models.Model):
    title = models.TextField(max_length=255)
    description = models.TextField(blank=True)
    square_image = models.ImageField(upload_to="frames/")
    corner_image = models.ImageField(upload_to="frames/")
    horizontal_image = models.ImageField(upload_to="frames/")
    vertical_image = models.ImageField(upload_to="frames/")
    order = models.IntegerField()
    width = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

class Passepartout(models.Model):
    distance = models.IntegerField(unique=True)

