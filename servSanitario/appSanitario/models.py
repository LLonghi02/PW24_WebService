from django.db import models

class Cittadino(models.Model):
    CSSN = models.CharField(max_length=16, primary_key=True)  # assuming CSSN is unique and primary key
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    dataNascita = models.DateField()
    luogoNascita = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nome} {self.cognome}"

class Ospedale(models.Model):
    codice = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=100)
    città = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=200)
    direttoreSanitario = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Ricovero(models.Model):
    codOspedale = models.ForeignKey(Ospedale, on_delete=models.CASCADE)
    cod = models.CharField(max_length=10, primary_key=True)
    paziente = models.ForeignKey(Cittadino, on_delete=models.CASCADE)
    data = models.DateField()
    durata = models.IntegerField()
    motivo = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cod} - {self.paziente}"

class Patologia(models.Model):
    cod = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=100)
    criticità = models.IntegerField()

    def __str__(self):
        return self.nome

class PatologiaRicovero(models.Model):
    codOspedale = models.ForeignKey(Ospedale, on_delete=models.CASCADE)
    codRicovero = models.ForeignKey(Ricovero, on_delete=models.CASCADE)
    codPatologia = models.ForeignKey(Patologia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codRicovero} - {self.codPatologia}"

class PatologiaCronica(models.Model):
    codPatologia = models.OneToOneField(Patologia, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"PatologiaCronica: {self.codPatologia}"

class PatologiaMortale(models.Model):
    codPatologia = models.OneToOneField(Patologia, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"PatologiaMortale: {self.codPatologia}"
