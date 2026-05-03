from rest_framework import viewsets, status
from rest_framework.response import Response
from EscuelaApp.models import Alumnos, Profesores
from EscuelaApp.api.serializer import AlumnoSerializer, ProfesorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import boto3
import uuid

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumnos.objects.all()
    serializer_class = AlumnoSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='fotoPerfil', parser_classes=[MultiPartParser, FormParser])
    def fotoPerfil(self, request, pk=None):
        file = request.FILES.get('foto')
        if not file:
            return Response({"error": "No se envió archivo"}, status=400)

        s3 = boto3.client('s3')
        bucket_name = '18003912-proyecto'
        filename = f"alumnos/{pk}/{uuid.uuid4()}_{file.name}"

        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={'ContentType': file.content_type}
        )

        url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"

        alumno = self.get_object()
        alumno.fotoPerfilUrl = url
        alumno.save()

        return Response({"fotoPerfilUrl": url}, status=200)



class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesores.objects.all()
    serializer_class = ProfesorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

'''
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
'''