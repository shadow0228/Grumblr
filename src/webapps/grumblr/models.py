from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
    text = models.CharField(max_length = 2000)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.text

class Profile(models.Model):
	owner = models.OneToOneField(User)
	age = models.CharField(max_length = 200, default = "Age", blank=True)
	bio = models.CharField(max_length = 420, default = "", blank=True)
	image = models.ImageField(upload_to = 'image', blank = True, default="/image/images.png")
	follows = models.ManyToManyField(User, related_name='followed_by')

class Comment(models.Model):
    text = models.CharField(max_length = 2000)
    post = models.ForeignKey(Post)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.text
# Create your models here.
