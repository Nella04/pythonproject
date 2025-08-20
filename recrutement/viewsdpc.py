from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Domaine
from .serializers import DomaineDetailSerializer

@api_view(['GET'])
def domaines_with_posts_and_competences(request):
    domaines = Domaine.objects.all()
    serializer = DomaineDetailSerializer(domaines, many=True)
    return Response(serializer.data)