import sqlite3

# WICHTIG: es muss eine überprüfung herein, ob die daten schon
# in der Datenbank sind
# nicht der relative pfad. sondern wirklich der richitge.
# es kann ein großen untershcied ggf. machen
# von wo aus die Datei geöffnet wird

conn = sqlite3.connect('db.sqlite3')  
cursor = conn.cursor()

aktivitaeten = [
    # Cardio
    "Laufen",
    "Radfahren",
    "Schwimmen",
    "Seilspringen",
    "Rudern",
    "Zumba",
    "HIIT",
    "Aqua-Fitness",
    "Nordic Walking",
    "Trampolinspringen",
    "Indoor Cycling (Spinning)",
    "Step-Aerobic",
    "Tanzen",
    "Ellipsentraining",
    "Laufband-Training",
    "Skipping Intervals",
    "Kickbox-Cardio",
    "Aerobic",
    "Trekking",
    "Inline-Skating",
    "Rollschuhfahren",
    "Cross-Trainer",
    "Tabata",
    "Wasserlaufen",
    "Jumping Fitness",
    "Stair Climbing",
    "Speed Hiking",
    "Aqua Jogging",
    "Body Attack",
    "Kick Aerobics",

    # Yoga
    "Yoga",

    "Bogenschießen", "Skispringen", "Biathlon", "Snowboardcross", "Eislaufen",
    "Eisschnelllauf", "BMX", "Triathlon", "Hindernislauf", "Orientierungslauf", "Parkour",
    "Freerunning", "Speed Climbing", "Bouldern", "Segeln", "Windsurfen", "Kitesurfen",
    "Drachenfliegen", "Paragliding", "Fallschirmspringen", "Bungee Jumping", "Tauchen",
    "Schnorcheln", "Freitauchen", "Rettungsschwimmen", "Paintball", "Airsoft", "Sumo",
    "Muay Thai", "Mixed Martial Arts (MMA)", "Slacklining", "Tchoukball", "Speerwurf",
    "Diskuswerfen", "Kugelstoßen", "Hammerwerfen", "Weitsprung", "Hochsprung",
    "Stabhochsprung", "Dreisprung", "Marathonlauf", "Race Walking", "Kampftanz",
    "Drift Trike", "Rennrodeln", "Skeleton", "Bobfahren", "Pelota", "Wakeboarding",
    "Jet-Skiing", "Motorsport", "Radsport", "Cheer-Tumbling", "Hockey", "Speedbadminton",

    # Outdoor-Aktivitäten
    "Wandern",
    "Klettern",
    "Skifahren",
    "Snowboarden",
    "Stand-Up Paddling",
    "Kajakfahren",
    "Rafting",
    "Canyoning",
    "Geocaching",
    "Mountainbiken",
    "Reiten",
    "Angeln",
    "Bogenschießen",
    "Golfen",
    "Surfen",
    "Höhlenforschung",
    "Klettersteiggehen",
    "Ziplining",
    "Schlittenfahren",
    "Eiswandern",
    "Sandboarding",
    "Fatbiking",
    "Paddeln",
    "Segeln",
    "Drachensteigen",
    "Schneeschuhwandern",
    "Trailrunning",
    "Trekking",
    "Orientierungslauf",
    "Slacklining"
   # Sportarten
    "Judo", "Tennis", "Fußball", "Basketball", "Volleyball", "Boxen", "Kickboxen",
    "Tanzen", "Pilates", "Crossfit", "Badminton", "Baseball", "Softball", "Cricket",
    "Handball", "Rugby", "American Football", "Eishockey", "Feldhockey", "Lacrosse",
    "Tischtennis", "Squash", "Bowling", "Karate", "Taekwondo", "Kung Fu", "Aikido",
    "Ringen", "Fechten", "Ballett", "Cheerleading", "Dart", "Boccia", "Schach (Sportdisziplin)",
    "Kampfsport allgemein", "Synchronschwimmen", "Wasserspringen", "Polo", "Wasserball"] 

# schreibt alle aktivitäten aus der Liste in die Datenbank 

for aktivität in aktivitaeten:
    cursor.execute('''
        INSERT INTO "workout_aktivitäten" (name, brechnungsgrundsatz) 
        VALUES (?, ?)
    ''', (aktivität, 'Standard'))
    print(aktivität)

# Änderungen speichern (commiten)
conn.commit()

# # Verbindung schließen
conn.close()

# print("Daten wurden erfolgreich in die Datenbank eingefügt.")

# # Liste der Aktivitäten


# # Standard-Berechnungsmethode
