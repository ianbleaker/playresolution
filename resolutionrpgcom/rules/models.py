from django.db import models

# Create your models here.
class Trait(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    short_description = models.CharField(max_length=200, blank=True)
    value = models.IntegerField(default=10)
    race_requisite = models.CharField(max_length=10, blank=True)
    trait_requisite = models.CharField(max_length=200, blank=True)
    