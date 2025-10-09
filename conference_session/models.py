from django.db import models
from conference.models import Conference

class Session(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='sessions')

    def __str__(self):
        return f"{self.title} ({self.conference.name})"
