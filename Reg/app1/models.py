from django.db import models

# Create your models here.
class PuzzlePiece(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
