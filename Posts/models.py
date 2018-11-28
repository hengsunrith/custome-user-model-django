# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage as storage
import tinify
import uuid
import os

tinify.key = "K8pTq8xf1BrFC33dqbV6wNbzHkqktWcr"

def get_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', filename)

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png','.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'jpg, png and jpeg are allowed.')

class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  text = models.TextField()
  image = models.FileField(upload_to=get_file_name,validators=[validate_file_extension])
  auto_delete = models.BooleanField(default=True, help_text="Auto Delete image unoptimized when uploaded.")
  
  created_date = models.DateTimeField(default=timezone.now())
  published_date = models.DateTimeField(blank=True, null=True)

  def publish(self):
    self.published_date = timezone.now()
    self.save()

  def __str__(self):
    return self.title

  def get_thumbnail(self):
    fh = storage.open(self.image.name)
    from_file = tinify.from_file(fh)

    resized_thumb = from_file.resize(
      method="thumb",
      width=300,
      height=300
    )

    image_path = str(os.path.splitext(str(fh))[0])
    extentions = str(os.path.splitext(str(fh))[1])

    if self.auto_delete == True:
      resized_thumb.to_file(image_path+"_optimized_"+extentions)
      os.rename(str(self.image.file.name), image_path+"_origin_"+extentions) #rename original photo
      os.rename(image_path+"_optimized_"+extentions, str(self.image.file.name)) #rename optimized to original str(self.image.file.name).
      os.remove(image_path+"_origin_"+extentions) #removing original photo

    else:
      resized_thumb.to_file(image_path+"_optimized_"+extentions)
      fh.close()

    return True

  def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # compress image size
        super(Post, self).save(force_update=force_update)
        if not self.get_thumbnail():
          raise Exception('Could not create optimation!')


class Book(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()