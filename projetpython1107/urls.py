from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recrutement import views
from recrutement.views import login_candidat
from recrutement.views import login_responsable
from recrutement.viewsdpc import domaines_with_posts_and_competences
from recrutement.views import delete_candidat_poste

router = DefaultRouter()
router.register(r'domaines', views.DomaineViewSet)
router.register(r'competences', views.CompetenceViewSet)
router.register(r'postes', views.PosteViewSet)
router.register(r'responsables', views.ResponsableViewSet)
router.register(r'candidats', views.CandidatViewSet)
router.register(r'appartenances', views.AppartenanceCompetencePosteViewSet)
router.register(r'candidat-competences', views.CandidatCompetenceViewSet)
router.register(r'tests', views.TestViewSet)
router.register(r'resultats', views.ResultatTestViewSet)
router.register(r'candidat-postes', views.CandidatPosteViewSet, basename='candidatposte')
from recrutement.views_password import password_reset_request, handle_reset_confirmation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login-candidat/', login_candidat, name='login-candidat'),
    path('api/login-responsable/', login_responsable, name='login-responsable'),
    path('api/domaines-details/', domaines_with_posts_and_competences, name='domaines-details'),
    path('api/candidat-poste/', delete_candidat_poste, name='delete-candidat-poste'),
    path('api/password-reset-request/', password_reset_request, name='password-reset-request'),
    path('api/handle-reset-confirmation/', handle_reset_confirmation, name='handle-reset-confirmation'),

]