from rest_framework import viewsets, status
from rest_framework.response import Response
from EscuelaApp.models import Alumnos, Profesores
from EscuelaApp.api.serializer import AlumnoSerializer, ProfesorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import boto3
import uuid
import time
import secrets

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

    @action(detail=True, methods=['post'], url_path='email')
    def email(self, request, pk=None):
        alumno = self.get_object()

        mensaje = f"""
            AlumnoId: {alumno.id}
            Nombre: {alumno.nombres} {alumno.apellidos}
            Matrícula: {alumno.matricula}
            Promedio: {alumno.promedio}
            """

        try:
            sns = boto3.client('sns', region_name='us-east-1')

            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-1:943587461590:AlumnosTopic',
                Message=mensaje,
                Subject='Información del alumno'
            )

            return Response({
                "message": "Mensaje enviado",
                "messageId": response.get('MessageId')
            }, status=200)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)

    @action(detail=True, methods=['post'], url_path='session/login')
    def login(self, request, pk=None):

        password = request.data.get('password')

        if not password:
            return Response(
                {"error": "Password requerida"},
                status=400
            )

        alumno = self.get_object()

        # Comparación simple
        if alumno.password != password:
            return Response(
                {"error": "Credenciales inválidas"},
                status=400
            )
        
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('sesiones_alumnos')

        session_id = str(uuid.uuid4())
        session_string = secrets.token_hex(64)
        
        table.put_item(
            Item={
                'sessionString': session_string,
                'id': session_id,
                'fecha': int(time.time()),
                'alumnoId': int(pk),
                'active': True
            }
        )

        return Response({
            "sessionId": session_id,
            "sessionString": session_string
        }, status=200)

    @action(detail=True, methods=['post'], url_path='session/verify')
    def verify(self, request, pk=None):

        session_string = request.data.get('sessionString')

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('sesiones_alumnos')

        response = table.get_item(
            Key={
                'sessionString': session_string
            }
        )
        item = response.get('Item')

        if not item:
            return Response(
                {"error": "sessionString requerido"},
                status=400
            )
        
        if item['alumnoId'] != int(pk):
            return Response({"error": "Alumno incorrecto"}, status=400)
        
        if not item['active']:
            return Response({"error": "Sesión no activa"}, status=400)

        return Response({
            "valid": True
        }, status=200)

    @action(detail=True, methods=['post'], url_path='session/logout')
    def logout(self, request, pk=None):

        session_string = request.data.get('sessionString')

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('sesiones_alumnos')

        response = table.get_item(
            Key={
                'sessionString': session_string
            }
        )
        item = response.get('Item')

        if not item:
            return Response(
                {"error": "Sesión inválida"}
            , status=400)

        table.update_item(
            Key={
                'sessionString': session_string
            },
            UpdateExpression="SET active = :a",
            ExpressionAttributeValues={
                ':a': False
            }
        )

        return Response({
            "message": "Sesión cerrada"
        }, status=200)

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesores.objects.all()
    serializer_class = ProfesorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
