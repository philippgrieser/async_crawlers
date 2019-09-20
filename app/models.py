from django.db import models
from django.utils import timezone

import datetime


class AnfemaProjects(models.Model):
    anfema = "anfema"
    description = "nice"


class Meta(models.Model):
    client = models.CharField(max_length=256)
    color = models.CharField(max_length=256)
    hidden = models.BooleanField()
    identification = models.CharField(max_length=256, null=False)
    span = models.CharField(max_length=256)
    title = models.CharField(max_length=256)

    def __str__(self):
        return "Meta " + str(self.id) + " " + str(self.identification)


class File(models.Model):
    file = models.CharField(max_length=256, null=False)
    meta = models.OneToOneField(Meta, on_delete=models.CASCADE)
    sorting = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(AnfemaProjects, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "File " + str(self.id) + " " + str(self.file)

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)
