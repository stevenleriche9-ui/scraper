import csv
import os
import urllib.request

import config
from models.produit import Produit, parser_prix
from scraper_utile.scraper import ScraperAmazon


CHAMPS = ["titre", "nom", "prix", "url_img", "categorie", "image"]

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
 "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def creer_dossier(chemin):
    if not os.path.exists(chemin):
        os.makedirs(chemin)


def produit_en_ligne(p):
    if p.prix is None:
        prix = ""
    else:
        prix = f"{p.prix:.2f}".replace(".", ",")
    return [p.titre, p.nom, prix, p.url_img, p.categorie, p.image]


def ecrire_resultats(produits):
    creer_dossier(config.DOSSIER_DATA)
    fichier = open(config.FICHIER_RESULTATS, "w", encoding="utf-8-sig", newline="")
    ecrivain = csv.writer(fichier, delimiter=config.SEPARATEUR_CSV)
    ecrivain.writerow(CHAMPS)
    for p in produits:
        ecrivain.writerow(produit_en_ligne(p))
    fichier.close()


def lire_resultats():
    produits = []
    if not os.path.exists(config.FICHIER_RESULTATS):
        return produits

    fichier = open(config.FICHIER_RESULTATS, "r", encoding="utf-8-sig", newline="")
    lecteur = csv.reader(fichier, delimiter=config.SEPARATEUR_CSV)
    premiere_ligne = True
    for ligne in lecteur:
        if premiere_ligne:          
            premiere_ligne = False
            continue
        if len(ligne) < 6:         
            continue
        p = Produit(ligne[0], ligne[1], parser_prix(ligne[2]), ligne[3], ligne[4], ligne[5])
        produits.append(p)
    fichier.close()
    return produits


def ecrire_par_categorie(produits):
    groupes = {}
    for p in produits:
        nom = p.categorie.strip().lower()
        if nom == "":
            nom = "sans categorie"
        if nom not in groupes:
            groupes[nom] = []
        groupes[nom].append(p)

    creer_dossier(config.DOSSIER_DATA)
    fichier = open(config.FICHIER_CATEGORIES, "w", encoding="utf-8-sig", newline="")
    ecrivain = csv.writer(fichier, delimiter=config.SEPARATEUR_CSV)
    ecrivain.writerow(CHAMPS)
    premier_bloc = True
    for liste in groupes.values():
        if not premier_bloc:
            ecrivain.writerow([])
            ecrivain.writerow([])
        premier_bloc = False
        for p in liste:
            ecrivain.writerow(produit_en_ligne(p))
    fichier.close()


def prochain_numero_image():
    plus_grand = 0
    for nom in os.listdir(config.DOSSIER_IMAGES):
        if not nom.startswith(config.PREFIXE_IMAGE):
            continue
        reste = nom[len(config.PREFIXE_IMAGE):]      # ex. "7.jpg"
        position_point = reste.find(".")
        if position_point < 1 or position_point == len(reste) - 1:
            continue
        chiffres = reste[:position_point]            # ex. "7"
        if chiffres.isdigit() and int(chiffres) > plus_grand:
            plus_grand = int(chiffres)
    return plus_grand + 1


def telecharger_images(produits):
    creer_dossier(config.DOSSIER_IMAGES)
    numero = prochain_numero_image()
    nb_ok = 0
    for p in produits:
        if p.url_img == "" or p.image != "":
            continue
        nom_fichier = config.PREFIXE_IMAGE + str(numero) + ".jpg"
        try:
            demande = urllib.request.Request(p.url_img, headers={"User-Agent": USER_AGENT})
            reponse = urllib.request.urlopen(demande, timeout=20)
            donnees = reponse.read()
            reponse.close()
            fichier = open(os.path.join(config.DOSSIER_IMAGES, nom_fichier), "wb")
            fichier.write(donnees)
            fichier.close()
        except Exception:
            continue       # image impossible à télécharger : on passe à la suivante
        p.image = nom_fichier
        numero = numero + 1
        nb_ok = nb_ok + 1
    return nb_ok


def nombre_de_pages(liste, taille=config.PRODUITS_PAR_ECRAN):
    nb = len(liste) // taille
    if len(liste) % taille != 0:
        nb = nb + 1
    if nb < 1:
        nb = 1
    return nb


def extraire_page(liste, numero, taille=config.PRODUITS_PAR_ECRAN):
    debut = (numero - 1) * taille
    return liste[debut:debut + taille]


class Controleur:
    def __init__(self):
        self.produits = lire_resultats()   
        self.derniere_recherche = ""

    def lancer_scraping(self, recherche, nb_pages, objectif):
        scraper = ScraperAmazon()
        try:
            scraper.ouvrir()
            scraper.scraper(recherche, nb_pages, objectif)
        finally:
            scraper.fermer()
            self.derniere_recherche = recherche
            nouveaux = self.ajouter(scraper.resultats)
            if len(nouveaux) > 0:  
                print("Téléchargement des images...")
                telecharger_images(nouveaux)
                self.sauvegarder()
        return len(nouveaux)

    def ajouter(self, trouves):
        nouveaux = []
        for p in trouves:
            existe_deja = False
            for autre in self.produits:
                if autre.categorie.lower() == p.categorie.lower() and autre.titre == p.titre:
                    existe_deja = True
                    break
            if not existe_deja:
                self.produits.append(p)
                nouveaux.append(p)
        return nouveaux

    def sauvegarder(self):
        ecrire_resultats(self.produits)
        ecrire_par_categorie(self.produits)
