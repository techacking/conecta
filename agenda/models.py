from django.db import models

# Create your models here.

class Entre(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    descricao = models.TextField()
    criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.criacao}'