from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-post', args=[self.pk])

class Comment(MPTTModel):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(default=timezone.now)
    
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def get_absolute_url(self):
        return reverse('blog-post', args=[self.post.pk])

    def __str__(self):
        return f"{self.author.username}@{self.post.pk}.{self.post.title[:25]} // {self.text[:50]}"

    class MPTTMeta:
            order_insertion_by = ['time_posted']
