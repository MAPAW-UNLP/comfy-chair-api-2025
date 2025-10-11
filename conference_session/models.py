from django.db import models
from conference.models import Conference

class Session(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    capacity = models.IntegerField()
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='session')

    def __str__(self):
        return f"{self.title} ({self.conference.title})"
