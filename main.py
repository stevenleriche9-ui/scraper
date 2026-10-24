from view.affichage import lancer

if __name__ == "__main__":
    try:
        lancer()
    except (KeyboardInterrupt, EOFError):
        print("\nAu revoir !")
