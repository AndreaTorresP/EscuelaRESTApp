from rest_framework import serializers
from EscuelaApp.models import Alumnos, Profesores

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnos
        fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesores
        fields = '__all__'