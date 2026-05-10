import uuid
from django.db import models

class Alumnos(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    promedio = models.FloatField()
    fotoPerfilUrl = models.URLField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=100)

class AlumnoSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.BigIntegerField()
    alumnoId = models.IntegerField()
    active = models.BooleanField(default=True)
    sessionString = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = 'sesiones_alumnos'

class Profesores(models.Model):
    numeroEmpleado = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    horasClase = models.IntegerField()