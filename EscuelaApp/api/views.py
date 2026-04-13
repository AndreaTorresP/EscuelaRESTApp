from rest_framework import viewsets, status
from rest_framework.response import Response
from EscuelaApp.api.serializer import AlumnoSerializer, ProfesorSerializer

ALUMNOS = []
PROFESORES = []

class AlumnoViewSet(viewsets.ViewSet):

    def list(self, request):
        if len(ALUMNOS) == 0:
            return Response({"message": "application/json []"}, status=200)
        return Response(ALUMNOS)

    def create(self, request):
        serializer = AlumnoSerializer(data=request.data)

        if serializer.is_valid():
            new_item = serializer.validated_data
            
            if "id" in request.data:
                new_item["id"] = request.data["id"]
            else:
                new_item["id"] = len(ALUMNOS) + 1

            ALUMNOS.append(new_item)
            return Response(new_item, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        for item in ALUMNOS:
            if int(item["id"]) == int(pk):
                return Response(item)
        return Response({"error": "No encontrado"}, status=404)

    def update(self, request, pk=None):
        for i, item in enumerate(ALUMNOS):
            if int(item["id"]) == int(pk):
                serializer = AlumnoSerializer(data=request.data)

                if serializer.is_valid():
                    updated = serializer.validated_data
                    updated["id"] = item["id"]
                    ALUMNOS[i] = updated
                    return Response(updated, status=200)

                return Response(serializer.errors, status=400)

        return Response({"error": "No encontrado"}, status=404)

    def destroy(self, request, pk=None):
        global ALUMNOS

        for item in ALUMNOS:
            if int(item["id"]) == int(pk):
                ALUMNOS = [a for a in ALUMNOS if int(a["id"]) != int(pk)]
                return Response(status=200)

        return Response({"error": "No encontrado"}, status=404)

class ProfesorViewSet(viewsets.ViewSet):

    def list(self, request):
        return Response(PROFESORES)

    def create(self, request):
        serializer = ProfesorSerializer(data=request.data)

        if serializer.is_valid():
            new_item = serializer.validated_data
            
            if "id" in request.data:
                new_item["id"] = request.data["id"]
            else:
                new_item["id"] = len(PROFESORES) + 1

            PROFESORES.append(new_item)
            return Response(new_item, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        for item in PROFESORES:
            if int(item["id"]) == int(pk):
                return Response(item)
        return Response({"error": "No encontrado"}, status=404)

    def update(self, request, pk=None):
        for i, item in enumerate(PROFESORES):
            if int(item["id"]) == int(pk):
                serializer = ProfesorSerializer(data=request.data)

                if serializer.is_valid():
                    updated = serializer.validated_data
                    updated["id"] = item["id"]
                    PROFESORES[i] = updated
                    return Response(updated, status=200)

                return Response(serializer.errors, status=400)

        return Response({"error": "No encontrado"}, status=404)

    def destroy(self, request, pk=None):
        global PROFESORES

        for item in PROFESORES:
            if int(item["id"]) == int(pk):
                PROFESORES = [a for a in PROFESORES if int(a["id"]) != int(pk)]
                return Response(status=200)

        return Response({"error": "No encontrado"}, status=404)
