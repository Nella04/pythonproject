
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Candidat
from datetime import datetime, timedelta
from django.utils import timezone
import secrets
from .serializers import CandidatSerializer
from django.conf import settings  

settings.DEFAULT_FROM_EMAIL


@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    
    try:
        candidat = Candidat.objects.get(email=email)
    except Candidat.DoesNotExist:
        return Response({'error': 'Aucun candidat avec cet email'}, status=status.HTTP_404_NOT_FOUND)
    
    # Générer un token
    token = candidat.generate_reset_token()
    
    # Créer les liens de confirmation
    confirm_link = f"http://localhost:3000/confirm-reset?token={token}&action=confirm"
    deny_link = f"http://localhost:3000/confirm-reset?token={token}&action=deny"
    
    # Préparer l'email HTML
    context = {
        'nom': candidat.nom,
        'prenom': candidat.prenom,
        'date': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'confirm_link': confirm_link,
        'deny_link': deny_link
    }
    
    html_content = render_to_string('email_password_reset.html', context)
    text_content = strip_tags(html_content)
    
    # Envoyer l'email
    email = EmailMultiAlternatives(
        "Confirmation de réinitialisation - Skills Metriks",
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [candidat.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    return Response({'message': 'Email de confirmation envoyé'})

@api_view(['GET'])
def handle_reset_confirmation(request):
    token = request.GET.get('token')
    action = request.GET.get('action')  # 'confirm' ou 'deny'
    
    try:
        candidat = Candidat.objects.get(reset_token=token, reset_token_used=False)
        
        # Vérifier si le token a expiré (1 heure de validité)
        if candidat.reset_token_created_at < timezone.now() - timedelta(hours=1):
            return Response({'error': 'Lien expiré'}, status=status.HTTP_400_BAD_REQUEST)
            
        if action == 'confirm':
            # Marquer le token comme utilisé
            candidat.reset_token_used = True
            candidat.save()
            
            # Retourner les informations du candidat
            serializer = CandidatSerializer(candidat)
            return Response({
                'message': 'Confirmation réussie',
                'candidat': serializer.data
            })
        
        elif action == 'deny':
            # Marquer le token comme utilisé et loguer la tentative
            candidat.reset_token_used = True
            candidat.save()
            log_security_alert(candidat)
            
            return Response({
                'message': 'Tentative signalée',
                'alert': 'Une alerte de sécurité a été enregistrée'
            })
            
    except Candidat.DoesNotExist:
        return Response({'error': 'Lien invalide ou déjà utilisé'}, status=status.HTTP_400_BAD_REQUEST)

def log_security_alert(candidat):
    # Ici vous pouvez logger la tentative dans votre système
    print(f"Alerte sécurité: Tentative de réinitialisation refusée pour {candidat.email}")