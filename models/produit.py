"""Produit : une classe simple + des fonctions pour nettoyer les textes d'Amazon."""

CHIFFRES = "0123456789"
LETTRES_ET_SIGNES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'&+-"


def parser_prix(texte):
    """Transforme '1 299,99 €' en 1299.99 (renvoie None s'il n'y a pas de prix)."""
    if texte is None or texte == "":
        return None

    # on enlève les espaces (normal, insécable, fin insécable)
    propre = texte.replace("\u202f", "").replace("\xa0", "").replace(" ", "")
    # si le prix a une virgule, les points sont des séparateurs de milliers
    if "," in propre:
        propre = propre.replace(".", "")

    # on avance jusqu'au premier chiffre
    i = 0
    while i < len(propre) and propre[i] not in CHIFFRES:
        i = i + 1
    if i == len(propre):
        return None

    # on lit la partie entière
    nombre = ""
    while i < len(propre) and propre[i] in CHIFFRES:
        nombre = nombre + propre[i]
        i = i + 1

    # on lit les décimales (après une virgule ou un point)
    if i + 1 < len(propre) and (propre[i] == "," or propre[i] == ".") and propre[i + 1] in CHIFFRES:
        nombre = nombre + "."
        i = i + 1
        while i < len(propre) and propre[i] in CHIFFRES:
            nombre = nombre + propre[i]
            i = i + 1

    return float(nombre)


def caractere_de_mot(c):
    """Vrai si le caractère peut faire partie d'un mot (lettre, chiffre, accent, ' & + -)."""
    if c in LETTRES_ET_SIGNES:
        return True
    if c >= "À" and c <= "ÿ":
        return True
    return False


def decouper_en_mots(titre):
    """'Apple iPhone 15 (128 Go)' -> ['Apple', 'iPhone', '15', '128', 'Go']"""
    if titre is None:
        titre = ""
    mots = []
    mot = ""
    for c in titre:
        if caractere_de_mot(c):
            mot = mot + c
        else:
            if mot != "":
                mots.append(mot)
                mot = ""
    if mot != "":
        mots.append(mot)
    return mots


def nom_court(titre, nb_mots=3):
    """'Apple iPhone 15 128 Go Noir' -> 'Apple iPhone 15'"""
    mots = decouper_en_mots(titre)
    return " ".join(mots[:nb_mots])


class Produit:
    def __init__(self, titre, nom, prix=None, url_img="", categorie="", image=""):
        self.titre = titre            # titre complet affiché sur Amazon
        self.nom = nom                # nom court (marque + modèle)
        self.prix = prix              # en euros, None s'il n'y a pas de prix
        self.url_img = url_img        # lien de l'image
        self.categorie = categorie    # mot recherché (ex. "iphone")
        self.image = image            # nom du fichier image enregistré (ex. imageproduit1.jpg)

    def correspond(self, recherche):
        """Vrai si le titre commence par, ou contient, ce que l'utilisateur a saisi."""
        return recherche.strip().lower() in self.titre.lower()

    def prix_texte(self):
        if self.prix is None:
            return "Pas de prix"
        return f"{self.prix:.2f} €".replace(".", ",")

    def texte(self):
        """Le produit sous forme de texte, pour l'affichage dans la console."""
        image = self.image
        if image == "":
            image = "non téléchargée"
        url = self.url_img
        if url == "":
            url = "aucune"
        return (self.nom + " | " + self.prix_texte() + "\n"
                + "   Titre     : " + self.titre + "\n"
                + "   Catégorie : " + self.categorie + "\n"
                + "   Image     : " + image + "\n"
                + "   URL image : " + url)
