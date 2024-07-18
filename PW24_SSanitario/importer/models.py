# importer/models.py

from django.db import models

class Cittadino(models.Model):
    CSSN = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    dataNascita = models.DateField(null=True, blank=True)
    luogoNascita = models.CharField(max_length=100, null=True, blank=True)
    indirizzo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} {self.cognome}"

class Ospedale(models.Model):
    codice = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=100)
    città = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=200, null=True, blank=True)
    direttoreSanitario = models.ForeignKey(Cittadino, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

class Patologia(models.Model):
    cod = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=50)
    criticità = models.IntegerField()

    def __str__(self):
        return self.nome

class PatologiaCronica(models.Model):
    codPatologia = models.OneToOneField(Patologia, primary_key=True, on_delete=models.CASCADE)

class PatologiaMortale(models.Model):
    codPatologia = models.OneToOneField(Patologia, primary_key=True, on_delete=models.CASCADE)

class Ricovero(models.Model):
    cod = models.CharField(max_length=10, primary_key=True)
    codOspedale = models.ForeignKey(Ospedale, on_delete=models.CASCADE)
    paziente = models.ForeignKey(Cittadino, on_delete=models.CASCADE)
    date = models.DateField()
    durata = models.IntegerField()
    motivo = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ricovero {self.cod} per {self.paziente}"

class PatologiaRicovero(models.Model):
    codOspedale = models.ForeignKey(Ospedale, on_delete=models.CASCADE)
    codRicovero = models.ForeignKey(Ricovero, on_delete=models.CASCADE)
    codPatologia = models.ForeignKey(Patologia, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('codOspedale', 'codRicovero', 'codPatologia')
