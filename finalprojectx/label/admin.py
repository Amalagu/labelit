from django.contrib import admin
from .models import Review, ImageLabel, ImageSample, Project



admin.site.register(ImageLabel)
#admin.site.register(ImageSample)
#admin.site.register(Project)
admin.site.register(Review)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(ImageSample)
class ImageSampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')
# Register your models here.
