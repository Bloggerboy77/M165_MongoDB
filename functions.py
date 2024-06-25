import re
from pymongo import MongoClient

# Die Verbindung mit der Datenbank und Collection herstellen
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)

gamedb = client.spiele
pcgames_coll = gamedb.pcgames

#Spiele in der Datenbank einfügen

def neues_Spiel_einfuegen():
    neues_Spiel = {
        "Titel": input("Geben Sie den Titel des Spiels ein, welches Sie einfügen möchten:"),
        "Ausgabejahr": None,
        "Downloadzahlen": None,
        "Altersgrenze": None,
        "Art": None,
        "Wertung von 1-10": None
    }

    ausgabejahr_input = input("Geben Sie das Ausgabejahr des Spiels ein:")
    while True:
        try:
            neues_Spiel["Ausgabejahr"] = int(ausgabejahr_input)
            break
        except ValueError:
            print("Ungültige Eingabe, bitte geben Sie eine ganze Zahl ein.")
            ausgabejahr_input = input("Geben Sie erneut das Ausgabejahr des Spiels ein:")

    downloadzahlen_input = input("Geben Sie die Downloadzahlen des Spiels ein:")
    while True:
        try:
            neues_Spiel["Downloadzahlen"] = int(downloadzahlen_input)
            break
        except ValueError:
            print("Ungültige Eingabe, bitte geben Sie eine ganze Zahl ein.")
            downloadzahlen_input = input("Geben Sie erneut die Downloadzahlen des Spiels ein:")

    altersgrenze_input = input("Geben Sie die Altersgrenze des Spiels ein:")
    while True:
        try:
            neues_Spiel["Altersgrenze"] = int(altersgrenze_input)
            break
        except ValueError:
            print("Ungültige Eingabe, bitte geben Sie eine ganze Zahl ein.")
            altersgrenze_input = input("Geben Sie erneut die Altersgrenze des Spiels ein:")

    neues_Spiel["Art"] = input("Geben Sie die Art des Spiels ein:").split(',')
    while True:
        wertung_input = input("Geben Sie die Wertung von 1-10 ein:")
        try:
            neues_Spiel["Wertung von 1-10"] = int(wertung_input)
            break
        except ValueError:
            print("Ungültige Eingabe, bitte geben Sie eine ganze Zahl zwischen 1 und 10 ein.")

    Eingabedoc = pcgames_coll.insert_one(neues_Spiel)

    if Eingabedoc.acknowledged:
        print("Das Spiel wurde erfolgreich hinzugefügt, die Id lautet:", Eingabedoc.inserted_id)
    else:
        print("Es gab einen Fehler beim Hinzufügen des Spiels.")

#Spiele in der Datenbank bearbeiten/ändern

def Spiele_in_der_datenbank_ändern():
    spiel_Titel = input("Geben Sie den Spielnamen ein, bei dem Sie etwas ändern möchten:")
    existenz_Spiel = pcgames_coll.find_one({"Titel": spiel_Titel})

    if existenz_Spiel:
        print("Spiel gefunden, Die Aktuellen Informationen:")
        print(existenz_Spiel)

        Spiel_editiert = {
            "Titel": input("Geben Sie den neuen Titel ein, oder drücken Sie Enter, um nichts zu ändern:") or existenz_Spiel["Titel"],
            "Ausgabejahr": int(input("Geben Sie das neue Ausgabejahr ein, oder drücken Sie Enter, um nichts zu ändern:")) or existenz_Spiel["Ausgabejahr"],
            "Downloadzahlen": int(input("Geben Sie die neuen Downloadzahlen ein, oder drücken Sie Enter, um nichts zu ändern:")) or existenz_Spiel["Downloadzahlen"],
            "Altersgrenze": int(input("Geben Sie die neue Altersgrenze ein, oder drücken Sie Enter, um nichts zu ändern machen:")) or existenz_Spiel["Altersgrenze"],
            "Art": input("Geben Sie die neue Art des Spiels ein, oder drücken Sie Enter, um nichts zu ändern:") or existenz_Spiel["Art"],
            "Wertung von 1-10": int(input("Geben Sie die neue Wertung von 1-10 ein, oder drücken Sie Enter, um nichts zu ändern:")) or existenz_Spiel["Wertung von 1-10"]
        }

        pcgames_coll.update_one({"Titel": spiel_Titel}, {"$set": Spiel_editiert})
        print("Die Spielinformationen wurden aktualisiert.")
    else:
        print("Die Spielinformationen konnten nicht aktualisiert werden")

#Spiele in der Datenbank löschen

def Spiele_in_der_datenbank_loeschen():
    spiel_Titel1 = input("Geben Sie ein Spieltitel ein:")
    spiel_existenz = pcgames_coll.find_one({"Titel": spiel_Titel1})

    if spiel_existenz:
        print("Spiel existiert")
        print(spiel_existenz)

        bestätigung = input("Möchten Sie das Spiel wirklich Löschen? (ja/nein)").lower()

        if bestätigung == "ja":
            pcgames_coll.delete_one({"Titel": spiel_Titel1})
            print("Das Spiel wurde gelöscht")
        elif bestätigung == "nein":
            print("Das Löschen des Spiels wurde abgebrochen")
        else:
            print("Ungültige Eingabe. Bitte geben Sie 'ja' oder 'nein' ein")
    else:
        print("Spiel nicht gefunden")

#Spiele in der Datenbank aufrufen

def spiele_finden():
    Ausgabejahr = int(input("Geben Sie das Ausgabejahr ein:"))
    Downloadzahlen = int(input("Geben Sie die Downloadzahlen ein:"))
    Altersgrenze = int(input("Geben Sie die Altersgrenze ein:"))
    Art = input("Geben Sie die Art des Spiels ein (kommagetrennt):").split(',')
    Wertung = int(input("Geben Sie die Wertung von 1-10 ein:"))

    Artset = re.compile("|".join(re.escape(a.strip()) for a in Art), re.IGNORECASE)

    Kriterien = {
        "Ausgabejahr": {"$eq": Ausgabejahr},
        "Downloadzahlen": {"$lte": Downloadzahlen},
        "Altersgrenze": {"$eq": Altersgrenze},
        "Art": {"$regex": Artset},
        "Wertung von 1-10": {"$eq": Wertung}
    }

    anzahl_spiele = pcgames_coll.count_documents(Kriterien)

    if anzahl_spiele == 0:
        print("Es gibt leider kein Spiel, das den Kriterien entspricht.")
    else:
        spiele = pcgames_coll.find(Kriterien)
        for ergebnis in spiele:
            print("_id", ergebnis["_id"])
            print("Titel", ergebnis["Titel"])
            print("Ausgabejahr", ergebnis["Ausgabejahr"])
            print("Downloadzahlen", ergebnis["Downloadzahlen"])
            print("Altersgrenze", ergebnis["Altersgrenze"])
            print("Art", ergebnis["Art"])
            print("Wertung von 1-10", ergebnis["Wertung von 1-10"])

#Abfrage was der Benutzer tun will

def hauptprogramm():
    while True:
        try:
            Auswahl = int(input("Was möchten Sie mit dem Programm tun?: \n 1. Daten aus der Datenbank abrufen \n 2. Daten in die Datenbank einfügen \n 3. Daten in der Datenbank ändern \n 4. Daten in der Datenbank löschen \n 5. Beenden \n Aktion bitte eingeben:"))
            if Auswahl == 5:
                break 
            elif Auswahl not in [1, 2, 3, 4]:
                print("Ungültige Eingabe. Bitte geben Sie 1, 2, 3, 4 oder 5 ein.")
            else:
                if Auswahl == 1:
                    spiele_finden()
                elif Auswahl == 2:
                    neues_Spiel_einfuegen()
                elif Auswahl == 3:
                    Spiele_in_der_datenbank_ändern()
                elif Auswahl == 4:
                    Spiele_in_der_datenbank_loeschen()
                elif Auswahl == 5:
                    break
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie 1, 2, 3, 4 oder 5 ein.")

# Das Programm wird beendet
print("Das Programm wurde beendet.")



# Die Aktion wird entsprechend der Eingabe des Benutzers ausgeführt


if __name__ == "__main__":
    while True:
        try:
            Auswahl = int(input("Was möchten Sie mit dem Programm tun?: \n 1. Spiele finden \n 2. Daten in die Datenbank einfügen \n 3. Daten in der Datenbank ändern \n 4. Daten in der Datenbank löschen \n 5. Beenden \n Aktion bitte eingeben:"))
            if Auswahl == 1:
                spiele_finden()
            elif Auswahl == 5:
                print("Das Programm wurde beendet.")
                break
            elif Auswahl == 2:
                    neues_Spiel_einfuegen()
            elif Auswahl == 3:
                    Spiele_in_der_datenbank_ändern()
            elif Auswahl == 4:
                    Spiele_in_der_datenbank_loeschen()       
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie 1, 2, 3, 4 oder 5 ein.")







                