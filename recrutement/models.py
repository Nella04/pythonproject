from django.db import models
from django.contrib.auth.hashers import make_password

class Domaine(models.Model):
    nom_domaine = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom_domaine

class Competence(models.Model):
    nom_competence = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom_competence

class Poste(models.Model):
    nom_poste = models.CharField(max_length=100)
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom_poste



class Responsable(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    motdepasse = models.CharField(max_length=128)  # 128 caractères pour stocker les hash
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def save(self, *args, **kwargs):
        # Hash le mot de passe avant de sauvegarder
        if self.motdepasse and not self.motdepasse.startswith('pbkdf2_sha256$'):
            self.motdepasse = make_password(self.motdepasse)
        super().save(*args, **kwargs)

class Candidat(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    teste = models.BooleanField(default=False)
    motdepasse = models.CharField(max_length=128)
    
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_created_at = models.DateTimeField(blank=True, null=True)
    reset_token_used = models.BooleanField(default=False)

    
    def generate_reset_token(self):
        import secrets
        from django.utils import timezone
        self.reset_token = secrets.token_urlsafe(50)
        self.reset_token_created_at = timezone.now()
        self.reset_token_used = False
        self.save()
        return self.reset_token



    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def save(self, *args, **kwargs):
        # Hash le mot de passe avant de sauvegarder
        if self.motdepasse and not self.motdepasse.startswith('pbkdf2_sha256$'):
            self.motdepasse = make_password(self.motdepasse)
        super().save(*args, **kwargs)
        

class CandidatPoste(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)
    tester = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('candidat', 'poste')  # Empêche les doublons
        verbose_name = "Association Candidat-Poste"
        verbose_name_plural = "Associations Candidat-Poste"
    
    def __str__(self):
        return f"{self.candidat} - {self.poste} (Testé: {'Oui' if self.tester else 'Non'})"



class AppartenanceCompetencePoste(models.Model):
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    coefficient = models.FloatField()
    
    class Meta:
        unique_together = ('poste', 'competence')
    
    def __str__(self):
        return f"{self.poste} - {self.competence} (coeff: {self.coefficient})"

class CandidatCompetence(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    niveau = models.IntegerField()
    
    class Meta:
        unique_together = ('candidat', 'competence')
    
    def __str__(self):
        return f"{self.candidat} - {self.competence} (niveau: {self.niveau})"

class Test(models.Model):
    date_test = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Test #{self.id} - {self.candidat}"

class ResultatTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    niveau_evalue = models.IntegerField()
    
    class Meta:
        unique_together = ('test', 'competence')
    
    def __str__(self):
        return f"{self.test} - {self.competence} (niveau: {self.niveau_evalue})"