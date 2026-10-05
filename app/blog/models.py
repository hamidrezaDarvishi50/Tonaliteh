from django.db import models

# Create your models here.
from art.models import Art
from django.utils.text import slugify

class Blog(models.Model):
    title = models.CharField(max_length=255)
    
    author_name = models.CharField(max_length=255)
    author_description = models.TextField()

    table_of_contents = models.TextField()
    description = models.TextField()
    short_description = models.TextField()
    final_description = models.TextField()

    main_image = models.ImageField(upload_to="blogs/", null=True)

    arts = models.ManyToManyField(Art, related_name="blogs", blank=True)

    title_seo = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    meta_description = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class BlogFAQ(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="faqs")
    question = models.TextField()
    answer = models.TextField()