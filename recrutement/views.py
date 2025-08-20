from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Domaine, Competence, Poste, Responsable, Candidat,
    AppartenanceCompetencePoste, CandidatCompetence,
    Test, ResultatTest
)
from .serializers import (
    DomaineSerializer, CompetenceSerializer, PosteSerializer,
    ResponsableSerializer, CandidatSerializer,
    AppartenanceCompetencePosteSerializer, CandidatCompetenceSerializer,
    TestSerializer, ResultatTestSerializer
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Candidat
from .serializers import CandidatSerializer

class DomaineViewSet(viewsets.ModelViewSet):
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer

class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer

class PosteViewSet(viewsets.ModelViewSet):
    queryset = Poste.objects.all()
    serializer_class = PosteSerializer

class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer

class CandidatViewSet(viewsets.ModelViewSet):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer

class AppartenanceCompetencePosteViewSet(viewsets.ModelViewSet):
    queryset = AppartenanceCompetencePoste.objects.all()
    serializer_class = AppartenanceCompetencePosteSerializer

class CandidatCompetenceViewSet(viewsets.ModelViewSet):
    queryset = CandidatCompetence.objects.all()
    serializer_class = CandidatCompetenceSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class ResultatTestViewSet(viewsets.ModelViewSet):
    queryset = ResultatTest.objects.all()
    serializer_class = ResultatTestSerializer
# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CandidatPoste

@api_view(['DELETE'])
def delete_candidat_poste(request):
    candidat_id = request.query_params.get('candidat')
    poste_id = request.query_params.get('poste')
    
    if not candidat_id or not poste_id:
        return Response(
            {"error": "Les paramètres 'candidat' et 'poste' sont requis"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        association = CandidatPoste.objects.get(candidat_id=candidat_id, poste_id=poste_id)
        association.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    except CandidatPoste.DoesNotExist:
        return Response(
            {"error": "Association non trouvée"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

from rest_framework import viewsets
from .models import CandidatPoste
from .serializers import CandidatPosteSerializer

class CandidatPosteViewSet(viewsets.ModelViewSet):
    queryset = CandidatPoste.objects.all()
    serializer_class = CandidatPosteSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtres optionnels
        candidat_id = self.request.query_params.get('candidat_id')
        poste_id = self.request.query_params.get('poste_id')
        tester = self.request.query_params.get('tester')
        
        if candidat_id:
            queryset = queryset.filter(candidat_id=candidat_id)
        if poste_id:
            queryset = queryset.filter(poste_id=poste_id)
        if tester:
            queryset = queryset.filter(tester=tester.lower() == 'true')
        
        return queryset

@api_view(['POST'])
def login_candidat(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email et mot de passe requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        candidat = Candidat.objects.get(email=email)
    except Candidat.DoesNotExist:
        return Response(
            {'error': 'Aucun candidat trouvé avec cet email'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not check_password(password, candidat.motdepasse):
        return Response(
            {'error': 'Mot de passe incorrect'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = CandidatSerializer(candidat)
    return Response(serializer.data)


@api_view(['POST'])
def login_responsable(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email et mot de passe requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        responsable = Responsable.objects.get(email=email)
    except Responsable.DoesNotExist:
        return Response(
            {'error': 'Aucun responsable trouvé avec cet email'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not check_password(password, responsable.motdepasse):
        return Response(
            {'error': 'Mot de passe incorrect'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = ResponsableSerializer(responsable)
    return Response(serializer.data)
