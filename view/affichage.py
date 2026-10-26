import os

import config
from controller.controller import Controleur, nombre_de_pages, extraire_page

LARGEUR = 64


def ligne(caractere="="):
    print(caractere * LARGEUR)


def afficher_titre(texte):
    print()
    ligne()
    print(texte.center(LARGEUR))
    ligne()


def demander(question, defaut=""):
    if defaut != "":
        question = question + " [" + defaut + "]"
    reponse = input(question + " : ").strip()
    if reponse == "":
        return defaut
    return reponse


def demander_entier(question, defaut, minimum=1):
    while True:
        reponse = demander(question, str(defaut))
        if reponse.isdigit() and int(reponse) >= minimum:
            return int(reponse)
        print(f"  -> entre un nombre entier >= {minimum}")


def oui_non(question, defaut=False):
    if defaut:
        indication = "O/n"
    else:
        indication = "o/N"
    reponse = input(question + " (" + indication + ") : ").strip().lower()
    if reponse == "":
        return defaut
    return reponse == "o" or reponse == "oui" or reponse == "y" or reponse == "yes"


def afficher_page(liste, numero, total):
    numero_produit = (numero - 1) * config.PRODUITS_PAR_ECRAN + 1
    for p in extraire_page(liste, numero):
        print("\n#" + str(numero_produit) + "  " + p.texte())
        numero_produit = numero_produit + 1
    print()
    ligne("-")
    print(f"Page {numero}/{total} - {len(liste)} produit(s)")


def parcourir(ctrl):
    liste = ctrl.produits
    if len(liste) == 0:
        print("\nAucun produit à afficher.")
        return
    total = nombre_de_pages(liste)
    numero = 1
    while True:
        afficher_page(liste, numero, total)
        choix = input("[n] suivante  [p] précédente  [num] aller à la page  [q] retour : ").strip().lower()
        if choix == "q" or choix == "":
            return
        if choix == "n" and numero < total:
            numero = numero + 1
        elif choix == "p" and numero > 1:
            numero = numero - 1
        elif choix.isdigit() and int(choix) >= 1 and int(choix) <= total:
            numero = int(choix)
        else:
            print("Choix impossible.")


def nouvelle_recherche(ctrl):
    afficher_titre("NOUVELLE RECHERCHE")
    recherche = demander("Quel produit veux-tu scrapper ?")
    if recherche == "":
        return
    nb_pages = demander_entier("Nombre de pages à parcourir", 1)
    objectif = None
    if oui_non("Limiter le nombre de produits conservés ?", False):
        objectif = demander_entier("Nombre de produits voulus", 20)

    print("\nOuverture du navigateur... (Ctrl+C pour arrêter, les produits déjà trouvés sont gardés)")
    try:
        nb = ctrl.lancer_scraping(recherche, nb_pages, objectif)
    except KeyboardInterrupt:
        print("\nArrêt demandé.")
        return
    except Exception as erreur:
        print(f"\nErreur pendant le scraping : {erreur}")
        return

    dossier = os.path.basename(config.DOSSIER_DATA)
    print(f"\n{nb} nouveau(x) produit(s). Fichiers mis à jour dans {dossier}/ :")
    print("  - " + os.path.basename(config.FICHIER_RESULTATS))
    print("  - " + os.path.basename(config.FICHIER_CATEGORIES))
    print("  - image/")


def lancer():
    ctrl = Controleur()
    while True:
        afficher_titre("SCRAPER AMAZON.FR")
        print(f"Produits en mémoire : {len(ctrl.produits)}")
        print()
        print(" 1. Nouvelle recherche")
        print(" 2. Parcourir les résultats (pagination)")
        print(" 0. Quitter")
        choix = input("\nTon choix : ").strip()
        if choix == "0":
            print("À bientôt !")
            return
        elif choix == "1":
            nouvelle_recherche(ctrl)
        elif choix == "2":
            parcourir(ctrl)
        else:
            print("Choix invalide.")
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