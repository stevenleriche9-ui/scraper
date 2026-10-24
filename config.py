import os

URL = "https://www.amazon.fr/"


RACINE = os.path.dirname(os.path.abspath(__file__))
DOSSIER_DATA = os.path.join(RACINE, "data")
DOSSIER_IMAGES = os.path.join(DOSSIER_DATA, "image")
FICHIER_RESULTATS = os.path.join(DOSSIER_DATA, "resultats.csv")
FICHIER_CATEGORIES = os.path.join(DOSSIER_DATA, "resultat_categorie.csv")
PREFIXE_IMAGE = "imageproduit"
SEPARATEUR_CSV = ";"


PAUSE = (3, 9)
DELAI_FRAPPE = (0.1, 0.3)


selecteur = {
    "barre_recherche": "twotabsearchtextbox",
    "carte": "div[data-component-type='s-search-result']",
    "titre": "h2 span",
    "prix": "span.a-price span.a-offscreen",
    "image": "img.s-image",
    "page_suivante": "a.s-pagination-next",
}

PRODUITS_PAR_PAGE = 10  
PRODUITS_PAR_ECRAN = 5  