
import os
import subprocess
import sys

import config
from controller.controller import Controleur, nombre_de_pages, extraire_page


def demander_entier(question, defaut):
    reponse = input(question + " [" + str(defaut) + "] : ").strip()
    if reponse.isdigit() and int(reponse) > 0:
        return int(reponse)
    return defaut


def parcourir(ctrl):
    if len(ctrl.produits) == 0:
        print("\nAucun produit à afficher.")
        return
    total = nombre_de_pages(ctrl.produits)
    numero = 1
    while True:
        for p in extraire_page(ctrl.produits, numero):
            print("\n" + p.texte())
        choix = input("\nPage " + str(numero) + "/" + str(total) + " - [n] suivante  [p] précédente  [autre] retour : ").strip().lower()
        if choix == "n" and numero < total:
            numero = numero + 1
        elif choix == "p" and numero > 1:
            numero = numero - 1
        elif choix != "n" and choix != "p":
            return


def nouvelle_recherche(ctrl):
    recherche = input("\nQuel produit veux-tu scrapper ? ").strip()
    if recherche == "":
        return
    nb_pages = demander_entier("Nombre de pages à parcourir", 1)
    objectif = None
    if input("Limiter le nombre de produits conservés ? (o/N) : ").strip().lower() == "o":
        objectif = demander_entier("Nombre de produits voulus", 20)

    print("\nOuverture du navigateur... (Ctrl+C pour arrêter)")
    try:
        nb = ctrl.lancer_scraping(recherche, nb_pages, objectif)
    except KeyboardInterrupt:
        print("\nArrêt demandé.")
        return
    except Exception as erreur:
        print("\nErreur pendant le scraping : " + str(erreur))
        return

    print("\nEnregistrement dans la base SQLite...")
    subprocess.run([sys.executable, os.path.join(config.RACINE, "enregistrer_base.py")])
    print("\n" + str(nb) + " nouveau(x) produit(s) ajouté(s).")


def lancer():
    ctrl = Controleur()
    while True:
        print("\n=== SCRAPER AMAZON.FR === (" + str(len(ctrl.produits)) + " produits en mémoire)")
        print("1. Nouvelle recherche")
        print("2. Parcourir les résultats")
        print("0. Quitter")
        choix = input("Ton choix : ").strip()
        if choix == "0":
            return
        elif choix == "1":
            nouvelle_recherche(ctrl)
        elif choix == "2":
            parcourir(ctrl)
        else:
            print("Choix invalide.")