from rest_framework import serializers
from .models import (
    Domaine, Competence, Poste, Responsable, Candidat,
    AppartenanceCompetencePoste, CandidatCompetence,
    Test, ResultatTest,CandidatPoste
)

class DomaineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domaine
        fields = '__all__'

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = '__all__'

class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__'

class CandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = '__all__'

class AppartenanceCompetencePosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppartenanceCompetencePoste
        fields = '__all__'

class CandidatCompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatCompetence
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class ResultatTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultatTest
        fields = '__all__'


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id', 'nom_competence']

class CandidatPosteSerializer(serializers.ModelSerializer):
    candidat_nom = serializers.CharField(source='candidat.nom', read_only=True)
    candidat_prenom = serializers.CharField(source='candidat.prenom', read_only=True)
    candidat_id = serializers.CharField(source='candidat.id', read_only=True)
    poste_nom = serializers.CharField(source='poste.nom_poste', read_only=True)
    poste_id = serializers.CharField(source='poste.id', read_only=True)
    domaine_nom = serializers.CharField(source='poste.domaine.nom_domaine', read_only=True)
    
    class Meta:
        model = CandidatPoste
        fields = ['id','candidat_id' ,'candidat', 'poste_id','poste', 'tester', 
                 'candidat_nom', 'candidat_prenom', 
                 'poste_nom', 'domaine_nom']
        extra_kwargs = {
            'candidat': {'write_only': True},
            'poste': {'write_only': True}
        }

# class AppartenanceCompetencePosteSerializer(serializers.ModelSerializer):
#     competence = CompetenceSerializer()
    
#     class Meta:
#         model = AppartenanceCompetencePoste
#         fields = ['competence', 'coefficient']
class AppartenanceCompetencePosteSerializer(serializers.ModelSerializer):
    poste_nom = serializers.CharField(source='poste.nom_poste', read_only=True)
    competence_nom = serializers.CharField(source='competence.nom_competence', read_only=True)
    id_comp = serializers.IntegerField(source='competence.id')
    
    class Meta:
        model = AppartenanceCompetencePoste
        fields = ['id','id_comp', 'poste', 'poste_nom', 'competence', 'competence_nom', 'coefficient']
        extra_kwargs = {
            'poste': {'write_only': True},
            'competence': {'write_only': True}
        }

class PosteDetailSerializer(serializers.ModelSerializer):
    competences = serializers.SerializerMethodField()
    
    class Meta:
        model = Poste
        fields = ['id', 'nom_poste', 'competences']
    
    def get_competences(self, obj):
        appartenances = AppartenanceCompetencePoste.objects.filter(poste=obj)
        serializer = AppartenanceCompetencePosteSerializer(appartenances, many=True)
        return serializer.data

class DomaineDetailSerializer(serializers.ModelSerializer):
    postes = serializers.SerializerMethodField()
    
    class Meta:
        model = Domaine
        fields = ['id', 'nom_domaine', 'postes']
    
    def get_postes(self, obj):
        postes = Poste.objects.filter(domaine=obj)
        serializer = PosteDetailSerializer(postes, many=True)
        return serializer.data