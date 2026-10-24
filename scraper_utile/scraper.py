"""Scraper Amazon.fr : recherche, lecture des produits, pagination."""
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
from config import selecteur
from models.produit import Produit, nom_court, parser_prix
from scraper_utile.driver import creer_driver, pause


class ScraperAmazon:
    def __init__(self):
        self.driver = None
        self.resultats = []   # les produits gardés (remplie au fur et à mesure)

    # ------------------------------------------------------------ ouvrir / fermer Chrome
    def ouvrir(self):
        self.driver = creer_driver()

    def fermer(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    # ------------------------------------------------------------ recherche
    def rechercher(self, recherche):
        self.driver.get(config.URL)
        pause()
        barre = self.driver.find_element(By.ID, selecteur["barre_recherche"])
        for lettre in recherche:
            barre.send_keys(lettre)
            time.sleep(random.uniform(config.DELAI_FRAPPE[0], config.DELAI_FRAPPE[1]))
        barre.send_keys(Keys.ENTER)
        pause()

    # ------------------------------------------------------------ lecture d'un produit
    def lire_carte(self, carte, categorie):
        """Lit une carte produit. Renvoie un Produit, ou None si on n'a pas trouvé de titre."""
        try:
            titre = carte.find_element(By.CSS_SELECTOR, selecteur["titre"]).text
        except Exception:
            return None
        if titre is None or titre == "":
            return None

        try:
            texte_prix = carte.find_element(By.CSS_SELECTOR, selecteur["prix"]).get_attribute("textContent")
            prix = parser_prix(texte_prix)
        except Exception:
            prix = None

        try:
            url_img = carte.find_element(By.CSS_SELECTOR, selecteur["image"]).get_attribute("src")
            if url_img is None:
                url_img = ""
        except Exception:
            url_img = ""

        return Produit(titre, nom_court(titre), prix, url_img, categorie)

    # ------------------------------------------------------------ page suivante
    def page_suivante(self):
        """Clique sur 'Suivant'. Renvoie False s'il n'y a plus de page."""
        try:
            bouton = self.driver.find_element(By.CSS_SELECTOR, selecteur["page_suivante"])
        except Exception:
            return False
        classe = bouton.get_attribute("class")
        if classe is None:
            classe = ""
        if "s-pagination-disabled" in classe:
            return False
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton)
        bouton.click()
        pause()
        return True

    # ------------------------------------------------------------ scraping complet
    def scraper(self, recherche, nb_pages=1, objectif=None):
        """
        recherche : ce que l'utilisateur a tapé
        nb_pages  : nombre maximum de pages Amazon à parcourir
        objectif  : on s'arrête dès qu'on a gardé ce nombre de produits (None = pas de limite)

        Seul filtre : on garde un produit si son titre commence par, ou contient, la recherche.
        """
        self.resultats = []
        deja_vus = []
        self.rechercher(recherche)

        for numero in range(1, nb_pages + 1):
            print(f"--- Page {numero}/{nb_pages} ---")
            cartes = self.driver.find_elements(By.CSS_SELECTOR, selecteur["carte"])
            cartes = cartes[:config.PRODUITS_PAR_PAGE]

            for carte in cartes:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", carte)
                produit = self.lire_carte(carte, recherche)
                pause()   # pause entre chaque produit

                if produit is None:
                    continue
                if produit.titre in deja_vus:
                    continue
                deja_vus.append(produit.titre)

                if not produit.correspond(recherche):
                    print("  [ignoré] " + produit.titre[:70])
                    continue

                self.resultats.append(produit)
                print(f"  [{len(self.resultats)}] {produit.nom} - {produit.prix_texte()}")
                if objectif is not None and len(self.resultats) >= objectif:
                    return self.resultats

            if numero < nb_pages:
                if not self.page_suivante():
                    print("Plus de page suivante.")
                    break

        return self.resultats
