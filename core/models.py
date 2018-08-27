from django.contrib.gis.db import models
from uuid import uuid4


# Create your models here.
def post_directory_path_with_uuid(instance, filename):
    return '{}/{}'.format(instance.post_category, uuid4())

class PostCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    owner = models.ForeignKey('auth.user', related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    post_category = models.ForeignKey(PostCategory, related_name='post', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=post_directory_path_with_uuid, null=True, blank=True)

    class Meta:
        ordering = ('-createdDate',)

    def __str__(self):
        return self.title
