from django.db import models 

class Conference(models.Model): 
    title = models.CharField(max_length=200) 
    description = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    blind_kind = models.BooleanField(default=False)

    def __str__(self): 
        return self.title