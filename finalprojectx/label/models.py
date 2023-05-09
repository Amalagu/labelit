from picklefield.fields import PickledObjectField
from django.db import models
import uuid


from django.db.models.deletion import CASCADE
from users.models import Profile
#these are model abstracts from django extensions
from django_extensions.db.models import (
    TimeStampedModel,
	ActivatorModel
)






class ImageSample(models.Model):
    label = models.CharField(max_length=50, default='Image')
    uploaded = models.DateTimeField(auto_now_add = True)
    imagelabel = models.ManyToManyField('ImageLabel', blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, upload_to='project_images/', default='project_images/default.jpg')
    imagedata = PickledObjectField(default = dict)

    def __str__(self):
        return self.label
        
    class Meta:
    	ordering = ['-uploaded']


class Project(models.Model):
    manager = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    annotators = models.ManyToManyField(Profile, blank=True, related_name='annotationprojects')
    project_display_picture = models.ImageField(
        null=True, blank=True, upload_to='project_display_picture/', default="project_display_picture/default.jpg")
    featured_image = models.ManyToManyField(ImageSample, blank=True, related_name='parentprojects', default = 'default.jpg')
    #featured_image = models.ImageField(
    #    null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = [ '-created', 'title']

    """@property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url"""

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset



class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class ImageLabel(models.Model):
    name = models.CharField(max_length=200)
    value = models.TextField(max_length = 500, blank= True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)


    def __str__(self):
        return self.name
