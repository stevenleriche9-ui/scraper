CHIFFRES = "0123456789"
LETTRES_ET_SIGNES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'&+-"


def parser_prix(texte):
    if texte is None or texte == "":
        return None

    propre = texte.replace("\u202f", "").replace("\xa0", "").replace(" ", "")
    if "," in propre:
        propre = propre.replace(".", "")

    i = 0
    while i < len(propre) and propre[i] not in CHIFFRES:
        i = i + 1
    if i == len(propre):
        return None

    nombre = ""
    while i < len(propre) and propre[i] in CHIFFRES:
        nombre = nombre + propre[i]
        i = i + 1

    if i + 1 < len(propre) and (propre[i] == "," or propre[i] == ".") and propre[i + 1] in CHIFFRES:
        nombre = nombre + "."
        i = i + 1
        while i < len(propre) and propre[i] in CHIFFRES:
            nombre = nombre + propre[i]
            i = i + 1

    return float(nombre)


def caractere_de_mot(c):
    if c in LETTRES_ET_SIGNES:
        return True
    if c >= "À" and c <= "ÿ":
        return True
    return False


def decouper_en_mots(titre):
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
    mots = decouper_en_mots(titre)
    return " ".join(mots[:nb_mots])


class Produit:
    def __init__(self, titre, nom, prix=None, url_img="", categorie="", image=""):
        self.titre = titre           
        self.nom = nom               
        self.prix = prix             
        self.url_img = url_img       
        self.categorie = categorie   
        self.image = image           

    def correspond(self, recherche):
        return recherche.strip().lower() in self.titre.lower()

    def prix_texte(self):
        if self.prix is None:
            return "Pas de prix"
        return f"{self.prix:.2f} €".replace(".", ",")

    def texte(self):
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
