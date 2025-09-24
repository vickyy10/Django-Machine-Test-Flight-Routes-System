from django.db import models
from django.core.validators import MinValueValidator
from core.constants import DIRECTION_CHOICES



class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.code} - {self.name}"



class Route(models.Model):
    
    from_airport = models.ForeignKey(Airport,on_delete=models.CASCADE, related_name='outgoing_routes')
    to_airport = models.ForeignKey(Airport,on_delete=models.CASCADE, related_name='incoming_routes')
    position = models.IntegerField(validators=[MinValueValidator(1)],help_text="Position in the route sequence")
    duration = models.IntegerField(validators=[MinValueValidator(1)],help_text="Duration in minutes")
    direction = models.CharField(max_length=1,choices=DIRECTION_CHOICES,default='R')
    
    class Meta:
        unique_together = ['from_airport', 'to_airport']
    
    def __str__(self):
        return f"{self.from_airport.code} → {self.to_airport.code}"