import sqlite3
from models import RawFood
import django
import os
from django.db import transaction

# Setze die Umgebungsvariable für das Django-Projekt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NutriFitAI.settings')

# Initialisiere Django
django.setup()

# Verbinden mit der alten Datenbank
old_db = '~/Schreibtisch/NutriFitAI/Anutri-database-test_backup.db'
conn = sqlite3.connect(old_db)
cursor = conn.cursor()

# SQL-Abfrage, um alle Datensätze aus der raw_foods Tabelle abzurufen
cursor.execute("SELECT * FROM raw_foods")

def get_raw_foods():
    conn = sqlite3.connect("~/Schreibtisch/NutriFitAI/Anutri-database-test_backup.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM raw_foods")
    foods = cursor.fetchall()
    conn.close()

    # Bereinigung der Daten
    def clean_data(value):
        if isinstance(value, str):
            value = value.strip('"')
            if value.replace('.', '', 1).isdigit():
                return float(value)
        return value

    foods = [
        [clean_data(item) for item in food]
        for food in foods
    ]
    return foods

# Bereinigte Daten abrufen
foods = get_raw_foods()

# Liste für RawFood-Objekte
raw_foods_to_create = []

# Durch alle Zeilen iterieren
for row in foods:
    try:
        # Validierung und Bereinigung der Daten
        raw_food = RawFood(
            name=row[0],
            kcal=float(row[1]) if row[1] else 0,
            fett=float(row[2]) if row[2] else 0,
            eiweiss=float(row[3]) if row[3] else 0,
            kohlenhydrate=float(row[4]) if row[4] else 0,
            ballaststoffe=float(row[5]) if row[5] else 0,
            salz=float(row[6]) if row[6] else 0,
            cholesterin=float(row[7]) if row[7] else 0,
            vitamin_a_retinolaequivalent=float(row[8]) if row[8] else 0,
            vitamin_a_retinoaktivitaet=float(row[9]) if row[9] else 0,
            retinol=float(row[10]) if row[10] else 0,
            beta_carotin=float(row[11]) if row[11] else 0,
            vitamin_b1_thiamin=float(row[12]) if row[12] else 0,
            vitamin_b2_riboflavin=float(row[13]) if row[13] else 0,
            vitamin_b3_niacin_nicotinsaure=float(row[14]) if row[14] else 0,
            vitamin_b3_niacinaequivalent=float(row[15]) if row[15] else 0,
            vitamin_b5_pantothensaure=float(row[16]) if row[16] else 0,
            vitamin_b6_pyridoxin=float(row[17]) if row[17] else 0,
            vitamin_b7_biotin=float(row[18]) if row[18] else 0,
            vitamin_b9_folsaeure=float(row[19]) if row[19] else 0,
            vitamin_b12_cobalamin=float(row[20]) if row[20] else 0,
            vitamin_c_ascorbinsaure=float(row[21]) if row[21] else 0,
            vitamin_d_calciferole=float(row[22]) if row[22] else 0,
            vitamin_e=float(row[23]) if row[23] else 0,
            vitamin_k=float(row[24]) if row[24] else 0,
            natrium=float(row[25]) if row[25] else 0,
            kalium=float(row[26]) if row[26] else 0,
            calcium=float(row[27]) if row[27] else 0,
            magnesium=float(row[28]) if row[28] else 0,
            phosphor=float(row[29]) if row[29] else 0,
            schwefel=float(row[30]) if row[30] else 0,
            chlorid=float(row[31]) if row[31] else 0,
            eisen=float(row[32]) if row[32] else 0,
            zink=float(row[33]) if row[33] else 0,
            kupfer=float(row[34]) if row[34] else 0,
            mangan=float(row[35]) if row[35] else 0,
            fluorid=float(row[36]) if row[36] else 0,
            iodid=float(row[37]) if row[37] else 0,
            mannit=float(row[38]) if row[38] else 0,
            sorbit=float(row[39]) if row[39] else 0,
            xylit=float(row[40]) if row[40] else 0,
            glucose=float(row[41]) if row[41] else 0,
            fructose=float(row[42]) if row[42] else 0,
            galactose=float(row[43]) if row[43] else 0,
            monosaccharide=float(row[44]) if row[44] else 0,
            saccharose=float(row[45]) if row[45] else 0,
            maltose=float(row[46]) if row[46] else 0,
            lactose=float(row[47]) if row[47] else 0,
            disaccharide=float(row[48]) if row[48] else 0,
            oligosaccharide_resorbierbar=float(row[49]) if row[49] else 0,
            oligosaccharide_nicht_resorbierbar=float(row[50]) if row[50] else 0,
            glykogen=float(row[51]) if row[51] else 0,
            staerke=float(row[52]) if row[52] else 0,
            polysaccharide=float(row[53]) if row[53] else 0,
            isoleucin=float(row[54]) if row[54] else 0,
            leucin=float(row[55]) if row[55] else 0,
            lysin=float(row[56]) if row[56] else 0,
            methionin=float(row[57]) if row[57] else 0,
            cystein=float(row[58]) if row[58] else 0,
            phenylalanin=float(row[59]) if row[59] else 0,
            tyrosin=float(row[60]) if row[60] else 0,
            threonin=float(row[61]) if row[61] else 0,
            tryptophan=float(row[62]) if row[62] else 0,
            valin=float(row[63]) if row[63] else 0,
            arginin=float(row[64]) if row[64] else 0,
            histidin=float(row[65]) if row[65] else 0,
            alanin=float(row[66]) if row[66] else 0,
            asparaginsaure=float(row[67]) if row[67] else 0,
            glutaminsaeure=float(row[68]) if row[68] else 0,
            glycin=float(row[69]) if row[69] else 0,
            prolin=float(row[70]) if row[70] else 0,
            serin=float(row[71]) if row[71] else 0,
            harnsaeure=float(row[72]) if row[72] else 0,
            purin=float(row[73]) if row[73] else 0,
            butansaure=float(row[74]) if row[74] else 0,
            hexansaure=float(row[75]) if row[75] else 0,
            octansaure=float(row[76]) if row[76] else 0,
            decansaure=float(row[77]) if row[77] else 0,
            dodecansaure=float(row[78]) if row[78] else 0,
            tetradecansaure=float(row[79]) if row[79] else 0,
            pentadecansaure=float(row[80]) if row[80] else 0,
            hexadecansaure=float(row[81]) if row[81] else 0,
            heptadecansaure=float(row[82]) if row[82] else 0,
            octadecansaure=float(row[83]) if row[83] else 0,
            eicosansaure=float(row[84]) if row[84] else 0,
            decosansaure=float(row[85]) if row[85] else 0,
            tetracosansaure=float(row[86]) if row[86] else 0,
            dokosansaure=float(row[87]) if row[87] else 0,
            cholin=float(row[88]) if row[88] else 0
        )
        raw_foods_to_create.append(raw_food)
    except Exception as e:
        print(f"Fehler beim Hinzufügen von Lebensmittel {row[0]}: {e}")

# Nutzung von bulk_create, um die Daten effizient hinzuzufügen
with transaction.atomic():
    RawFood.objects.bulk_create(raw_foods_to_create)

print("Daten erfolgreich hinzugefügt!")
