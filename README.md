# Scraper Amazon.fr

Application console (architecture MVC) qui scrape les résultats de recherche d'Amazon.fr avec Selenium.
On récupère seulement le **titre**, le **nom**, le **prix**, l'**URL de l'image** et l'**image**.
Une pause aléatoire de 3 à 9 secondes est faite entre chaque scrape.

## Lancer ces commande dans le terminal 
pip install -r requirements.txt
python main.py
Google Chrome doit être installé.

## Structure
scraper_amazon/
├── main.py            point d'entrée
├── config.py          URL, sélecteurs, pause, chemins
├── models/            produit.py (classe Produit + nettoyage prix/nom)
├── view/              affichage.py (menus et affichage console)
├── controller/        produits.py (contrôleur + CSV + images)
├── scraper_utile/     scraper.py, driver.py
└── data/              resultats.csv, resultat_categorie.csv, image/

## Résultats
- **`resultats.csv`** : une ligne par produit.
- **`resultat_categorie.csv`** : produits regroupés par catégorie (le mot recherché), blocs séparés par deux lignes vides.
- **`image/`** : `imageproduit1.jpg`, `imageproduit2.jpg`, etc.

## Fonctionnalités
- Menu console : recherche et résultats paginés.
- Seul filtre : un produit est gardé si son titre commence par, ou contient, ce que tu as saisi .

## Notes
- La pause se règle avec `PAUSE` dans `config.py`.
- En cas de CAPTCHA, résous-le dans la fenêtre Chrome.