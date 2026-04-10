from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AlumnoViewSet, ProfesorViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'alumnos', AlumnoViewSet, basename='alumnos')
router.register(r'profesores', ProfesorViewSet, basename='profesores')

urlpatterns = [
    path('', include(router.urls)),
]