import sqlite3
import os

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Benutzername und neuer Wert für is_pro
username = "hans"
is_pro = 1  # 1 = True, 0 = False

cursor.execute("""
UPDATE users_customuser
SET is_pro = ?
WHERE username = ?
""", (is_pro, username))

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()