from rest_framework import viewsets, status
from rest_framework.response import Response
from EscuelaApp.api.serializer import AlumnoSerializer, ProfesorSerializer
import json
import os

FILE_ALUMNOS = "alumnos.json"
FILE_PROFESORES = "profesores.json"

def read_file(FILE_PATH):
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def write_file(FILE_PATH,data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)

class AlumnoViewSet(viewsets.ViewSet):

    def list(self, request):
        ALUMNOS = read_file(FILE_ALUMNOS)
        if len(ALUMNOS) == 0:
            return Response({"message": "application/json []"}, status=200)
        return Response(ALUMNOS)

    def create(self, request):
        ALUMNOS = read_file(FILE_ALUMNOS)

        serializer = AlumnoSerializer(data=request.data)

        if serializer.is_valid():
            new_item = serializer.validated_data
            
            if "id" in request.data:
                new_item["id"] = request.data["id"]
            else:
                new_item["id"] = len(ALUMNOS) + 1

            ALUMNOS.append(new_item)
            write_file(FILE_ALUMNOS, ALUMNOS)

            return Response(new_item, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        ALUMNOS = read_file(FILE_ALUMNOS)

        for item in ALUMNOS:
            if int(item["id"]) == int(pk):
                return Response(item)
        return Response({"error": "No encontrado"}, status=404)

    def update(self, request, pk=None):
        ALUMNOS = read_file(FILE_ALUMNOS)

        for i, item in enumerate(ALUMNOS):
            if int(item["id"]) == int(pk):
                serializer = AlumnoSerializer(data=request.data)

                if serializer.is_valid():
                    updated = serializer.validated_data
                    updated["id"] = item["id"]
                    ALUMNOS[i] = updated
                    write_file(FILE_ALUMNOS, ALUMNOS)
                    
                    return Response(updated, status=200)

                return Response(serializer.errors, status=400)

        return Response({"error": "No encontrado"}, status=404)

    def destroy(self, request, pk=None):
        ALUMNOS = read_file(FILE_ALUMNOS)

        for item in ALUMNOS:
            if int(item["id"]) == int(pk):
                ALUMNOS = [a for a in ALUMNOS if int(a["id"]) != int(pk)]
                write_file(FILE_ALUMNOS, ALUMNOS)

                return Response(status=200)

        return Response({"error": "No encontrado"}, status=404)

class ProfesorViewSet(viewsets.ViewSet):

    def list(self, request):
        PROFESORES = read_file(FILE_PROFESORES)
        if len(PROFESORES) == 0:
            return Response({"message": "application/json []"}, status=200)
        return Response(PROFESORES)

    def create(self, request):
        PROFESORES = read_file(FILE_PROFESORES)

        serializer = ProfesorSerializer(data=request.data)

        if serializer.is_valid():
            new_item = serializer.validated_data
            
            if "id" in request.data:
                new_item["id"] = request.data["id"]
            else:
                new_item["id"] = len(PROFESORES) + 1

            PROFESORES.append(new_item)
            write_file(FILE_PROFESORES, PROFESORES)
            return Response(new_item, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        PROFESORES = read_file(FILE_PROFESORES)

        for item in PROFESORES:
            if int(item["id"]) == int(pk):
                return Response(item)
        return Response({"error": "No encontrado"}, status=404)

    def update(self, request, pk=None):
        PROFESORES = read_file(FILE_PROFESORES)

        for i, item in enumerate(PROFESORES):
            if int(item["id"]) == int(pk):
                serializer = ProfesorSerializer(data=request.data)

                if serializer.is_valid():
                    updated = serializer.validated_data
                    updated["id"] = item["id"]
                    PROFESORES[i] = updated
                    write_file(FILE_PROFESORES, PROFESORES)

                    return Response(updated, status=200)

                return Response(serializer.errors, status=400)

        return Response({"error": "No encontrado"}, status=404)

    def destroy(self, request, pk=None):
        PROFESORES = read_file(FILE_PROFESORES)

        for item in PROFESORES:
            if int(item["id"]) == int(pk):
                PROFESORES = [a for a in PROFESORES if int(a["id"]) != int(pk)]
                write_file(FILE_PROFESORES, PROFESORES)
                
                return Response(status=200)

        return Response({"error": "No encontrado"}, status=404)
