from django.db import models

# Create your models here.
class time_table(models.Model):
    name = models.CharField(max_length=200)
    writers = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    def __str__(self): 
        return self.name 