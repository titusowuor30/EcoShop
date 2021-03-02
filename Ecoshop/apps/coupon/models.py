from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Cupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(blank=True,null=True)
    valid_to = models.DateTimeField(blank=True,null=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    active = models.BooleanField()

    def __str__(self):
        return self.code
