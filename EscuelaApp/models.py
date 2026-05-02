from django.db import models

class Alumnos(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    promedio = models.FloatField()
    fotoPerfilUrl = models.URLField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=100)

class Profesores(models.Model):
    numeroEmpleado = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    horasClase = models.IntegerField()