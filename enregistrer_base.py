"""Lit data/resultats.csv et enregistre les produits dans data/base.sqlite3.
À lancer après un scraping :  python enregistrer_base.py"""
import csv
import os
import sqlite3

DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_CSV = os.path.join(DOSSIER, "data", "resultats.csv")
FICHIER_BASE = os.path.join(DOSSIER, "data", "base.sqlite3")


def texte_en_prix(texte):
    """'1299,99' -> 1299.99 ; texte vide -> None"""
    try:
        return float(texte.replace(",", "."))
    except ValueError:
        return None


if not os.path.exists(FICHIER_CSV):
    print("Fichier introuvable : " + FICHIER_CSV)
    raise SystemExit

fichier = open(FICHIER_CSV, "r", encoding="utf-8-sig", newline="")
lecteur = csv.reader(fichier, delimiter=";")
lignes = []
premiere_ligne = True
for ligne in lecteur:
    if premiere_ligne:         
        premiere_ligne = False
        continue
    if len(ligne) < 6:        
        continue
    lignes.append(ligne)
fichier.close()

connexion = sqlite3.connect(FICHIER_BASE)
curseur = connexion.cursor()

curseur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE
    )
""")
curseur.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        nom TEXT,
        prix REAL,
        url_img TEXT,
        image TEXT,
        categorie_id INTEGER NOT NULL,
        FOREIGN KEY (categorie_id) REFERENCES categories(id),
        UNIQUE (titre, categorie_id)
    )
""")

nouveaux = 0
for ligne in lignes:
    titre = ligne[0]
    nom = ligne[1]
    prix = texte_en_prix(ligne[2])
    url_img = ligne[3]
    categorie = ligne[4].strip().lower()
    image = ligne[5]
    if categorie == "":
        categorie = "sans categorie"

    curseur.execute("INSERT OR IGNORE INTO categories (nom) VALUES (?)", (categorie,))
    curseur.execute("SELECT id FROM categories WHERE nom = ?", (categorie,))
    categorie_id = curseur.fetchone()[0]

    curseur.execute(
        "INSERT OR IGNORE INTO produits (titre, nom, prix, url_img, image, categorie_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (titre, nom, prix, url_img, image, categorie_id))
    nouveaux = nouveaux + curseur.rowcount    

connexion.commit()
connexion.close()

print(str(len(lignes)) + " produit(s) lu(s) dans resultats.csv")
print(str(nouveaux) + " nouveau(x) ajouté(s) dans " + FICHIER_BASE)