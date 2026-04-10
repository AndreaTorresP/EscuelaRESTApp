from rest_framework import serializers

class AlumnoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=100)
    matricula = serializers.CharField(max_length=20)
    promedio = serializers.FloatField()

class ProfesorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    numeroEmpleado = serializers.CharField(max_length=20)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=100)
    horasClase = serializers.IntegerField()