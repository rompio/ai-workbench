import sqlite3

def get_raw_foods():
    conn = sqlite3.connect("Anutri-database-test_backup.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM raw_foods")
    foods = cursor.fetchall()
    conn.close()

    # Bereinigung der Daten
    def clean_data(value):
        if isinstance(value, str):
            # Entferne unnötige Anführungszeichen
            value = value.strip('"')
            # Konvertiere in Float, falls möglich
            if value.replace('.', '', 1).isdigit():
                return float(value)
        return value

    # Anwenden der Bereinigung auf alle Felder
    foods = [
        [clean_data(item) for item in food]
        for food in foods
    ]
    return foods
