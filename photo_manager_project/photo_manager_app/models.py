from django.core.exceptions import ValidationError
from django.db import models


def name_file(instance, filename):
    return '/'.join(['images', filename])


class Images(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.size
        megabyte_limit = 5
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    image = models.ImageField(upload_to=name_file, validators=[validate_image])
    date = models.DateField(blank=False, null=True)
    geolocation = models.TextField(max_length=400, default=None, null=True, blank=False)
    description = models.TextField(max_length=400, default=None, null=True, blank=False)

    def __str__(self):
        return self.geolocation


class People(models.Model):
    name = models.CharField(max_length=100, blank=False, null=True)
    image = models.ForeignKey(Images, related_name='people_in_photo', on_delete=models.CASCADE, blank=False, null=True)
