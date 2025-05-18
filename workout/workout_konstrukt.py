from .models import TrainingsplanÜbung

class Sat:
    """
    Represents a single set with a certain number of repeated sub-elements
    (i.e., Wiederholungen).
    """
    def __init__(self, satz_anzahl, wiederholungen):
        """
        :param satz_anzahl: integer number of sets
        :param wiederholungen: integer or list for how many reps per set
        """
        self.count = []
        # Ensure satz_anzahl is an integer (or 0 if invalid).
        if not isinstance(satz_anzahl, int):
            try:
                satz_anzahl = int(next(iter(satz_anzahl)))  # if it was a set/dict
            except Exception:
                satz_anzahl = 0

        for i in range(satz_anzahl):
            self.count.append(i + 1)
        if isinstance(wiederholungen, list):
            self.wiederholungen = wiederholungen
        else:
            # If it's just an integer, create a list of 1's that length
            self.wiederholungen = [1] * (wiederholungen or 0)

class Kraftübung:
    """
    Holds a single exercise and its sets.
    """
    def __init__(self, name, exercise_id):
        self.name = name
        self.id = exercise_id
        self.sätze = []

    def add_sat(self, sat_obj):
        self.sätze.append(sat_obj)

class Struktur:
    """
    Collects multiple Kraftübungen for a plan structure.
    """
    def __init__(self):
        self.kraftübungen = []

    def add_übung(self, übung_obj):
        self.kraftübungen.append(übung_obj)

def generiere_trainingsplan_struktur(trainingsplan_id):
    """
    Erstellt die Trainingsplan-Struktur basierend auf TrainingsplanÜbung-Einträgen
    in der Datenbank.
    """
    trainingsplan_übungen = TrainingsplanÜbung.objects.filter(trainingsplan_id=trainingsplan_id)
    struktur = Struktur()

    for übung in trainingsplan_übungen:
        kraftübung = Kraftübung(übung.übung.name, übung.übung.id)
        satz_anzahl = übung.satz or 0
        wiederholungen = übung.wiederholung or 0
        # Create a Sat object from these numbers
        sat = Sat(satz_anzahl, wiederholungen)
        kraftübung.add_sat(sat)
        struktur.add_übung(kraftübung)

    return struktur