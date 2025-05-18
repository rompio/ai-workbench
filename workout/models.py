from django.conf import settings
from django.db import models

class UserData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    größe = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.größe}"


class Coach(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    output = models.TextField(null=True, blank=True)
    input_text = models.TextField(null=True, blank=True)
    thema = models.CharField(max_length=200, null=True, blank=True)
    datum = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Coach for {self.user.username} - {self.thema}"


class KörperData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    körperfettanteil = models.FloatField(null=True, blank=True)
    muskelmasse = models.FloatField(null=True, blank=True)
    knochenmasse = models.FloatField(null=True, blank=True)
    fettmenge = models.FloatField(null=True, blank=True)
    wassermenge = models.FloatField(null=True, blank=True)
    datum = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.datum}"


class Körpertyp(models.Model):
    körpertyp = models.CharField(max_length=100)

    def __str__(self):
        return self.körpertyp


class KörpertyUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    körpertyp = models.ForeignKey(Körpertyp, on_delete=models.CASCADE)
    datum = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.körpertyp.körpertyp}"


class Gewicht(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gewicht = models.FloatField()
    datum = models.DateField()
    def __str__(self):
        return f"{self.user.username} - {self.gewicht}"


class Aktivitäten(models.Model):
    name = models.CharField(max_length=100)
    brechnungsgrundsatz = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class AktivitätenUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    aktivität = models.ForeignKey(Aktivitäten, on_delete=models.CASCADE)
    datum = models.DateField()
    dauer = models.FloatField(null=True, blank=True)
    distanz = models.FloatField(null=True, blank=True)
    puls = models.CharField(max_length=50, null=True, blank=True)
    max_puls = models.IntegerField(null=True, blank=True)
    höhenmeter = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.aktivität.name}"


class TrainingRoutine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    beschreibung = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Trainingsplan(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Trainingsplan_TrainingRoutine(models.Model):
    training_routine = models.ForeignKey(TrainingRoutine, on_delete=models.CASCADE)
    trainingsplan = models.ForeignKey(Trainingsplan, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Muskelgruppe(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class ÜbungenKrafttraining(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.TextField(null=True, blank=True)
    bild_path = models.TextField(null=True, blank=True)
    video_path = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class HauptNebenMuskel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ÜbungenKrafttrainingMuskelgruppe(models.Model):
    übung = models.ForeignKey(ÜbungenKrafttraining, on_delete=models.CASCADE)
    muskel = models.ForeignKey(HauptNebenMuskel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.übung.name} - {self.muskel.name}"

class TrainingsplanÜbung(models.Model):
    übung = models.ForeignKey(ÜbungenKrafttraining, on_delete=models.CASCADE)
    trainingsplan = models.ForeignKey(Trainingsplan, on_delete=models.CASCADE)
    satz = models.IntegerField(null=True, blank=True)
    wiederholung = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class KrafttrainingInstanz(models.Model):
    trainingsplan = models.ForeignKey(Trainingsplan, on_delete=models.CASCADE)
    datum = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.trainingsplan.name} - {self.datum}"


class TrainingsplanÜbungenKrafttraining(models.Model):
    übung = models.ForeignKey(ÜbungenKrafttraining, null=True, on_delete=models.CASCADE)
    instanz = models.ForeignKey(KrafttrainingInstanz, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.übung.name} - {self.instanz}"


class AusführungSatz(models.Model):
    training_übung = models.ForeignKey(TrainingsplanÜbungenKrafttraining, on_delete=models.CASCADE)
    satz_nummer = models.IntegerField()

    def __str__(self):
        return f"Satz {self.satz_nummer} - {self.training_übung}"


class AusführungWid(models.Model):
    ausführung = models.ForeignKey(AusführungSatz, on_delete=models.CASCADE)
    gewicht = models.FloatField()

    def __str__(self):
        return f"Gewicht {self.gewicht} - {self.ausführung}"
