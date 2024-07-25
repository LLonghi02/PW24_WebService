from django.db import models

class Cittadino(models.Model):
    CSSN = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    dataNascita = models.DateField(null=True, blank=True)
    luogoNascita = models.CharField(max_length=100, null=True, blank=True)
    indirizzo = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'Cittadino'
   
class Ospedale(models.Model):
    codice = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=100)
    città = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=200, null=True, blank=True)
    direttoreSanitario = models.ForeignKey(Cittadino, on_delete=models.PROTECT, db_column='direttoreSanitario')
    
    class Meta:
        db_table = 'Ospedale'

class Patologia(models.Model):
    cod = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=50)
    criticità = models.IntegerField()

    class Meta:
        db_table = 'Patologia'

class PatologiaCronica(models.Model):
    codPatologia = models.OneToOneField(Patologia, primary_key=True, on_delete=models.CASCADE,db_column='codPatologia')

    class Meta:
        db_table = 'PatologiaCronica'

class PatologiaMortale(models.Model):
    codPatologia = models.OneToOneField(Patologia, primary_key=True, on_delete=models.CASCADE,db_column='codPatologia')

    class Meta:
        db_table = 'PatologiaMortale'

class Ricovero(models.Model):
    cod = models.CharField(max_length=10, primary_key=True)
    codOspedale = models.ForeignKey(Ospedale, on_delete=models.CASCADE,db_column='codOspedale')
    paziente = models.ForeignKey(Cittadino, on_delete=models.CASCADE,db_column='paziente')
    data = models.DateField(null=True, blank=True)
    durata = models.IntegerField()
    motivo = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Ricovero'

class PatologiaRicovero(models.Model):
    codOspedale = models.ForeignKey(Ospedale, on_delete=models.CASCADE,db_column='codOspedale')
    codRicovero = models.ForeignKey(Ricovero, on_delete=models.CASCADE,db_column='codRicovero')
    codPatologia = models.ForeignKey(Patologia, on_delete=models.CASCADE,db_column='codPatologia')

    class Meta:
        unique_together = ('codOspedale', 'codRicovero', 'codPatologia')
        # Definisci la chiave primaria composta usando i campi

        db_table = 'PatologiaRicovero'

