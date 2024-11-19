from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)       

    def __str__(self):
        return f"{self.user.username}'s photo at {self.uploaded_at}"

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True)
    scene_data = models.JSONField(null=True)


