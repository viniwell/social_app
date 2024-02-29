from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images', on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    slug=models.SlugField(max_length=100, blank=True)
    url=models.URLField(max_length=2000)
    image=models.ImageField(upload_to='images/%y/%m/%d')
    description=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    class Meta:
        indexes= [
            models.Index(fields=['-created'])
        ]
        ordering=['-created']

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("images:image_detail", kwargs={"id":self.pk, "slug":self.slug})
    