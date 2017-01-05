#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modèle d'une table de jeu de cartes
construit sur le principe de Modèle-Vue-Contrôleur.
Ce module est celui du modèle.
Son interface est utilisée par le contrôleur uniquement.
Son contenu est connu et en partie modifié par la vue.
Il ne connaît rien du contrôleur ni de la vue.
Il connaît l'interface de la classe Jeu qu'il utilise
Il définit les classes et leurs interactions nécessaires à la table de jeu.
Copyrigth electron-libre de de www.fun-mooc.fr
Licence CeCill v2
novembre 2016
"""
# utilisé pour surveiller le tapis et autres objets de la table
from support import Observable
# utilisé quand il faut prendre une décision "au pif"
from random import randint

import logging
logger = logging.getLogger("modele")

class Joueur(Observable):
    """Joeur qui prend ses décisions aléatoirement"""
    def __init__(self, nom, visible = False):
        self.nom = nom
        # rend visibles ou non ses cartes
        self.visible = visible
        # les cartes dont dispose le joueur
        self.main = []
        # pour pouvoir signaler les changements d'état à la vue
        Observable.__init__(self)

    def recevoir(self, donne):
        """ ajoute la donne à la main du joueur"""
        # pour accepter les cas où la donne a une ou plusieurs cartes
        if hasattr(donne, '__getitem__'):
            self.main.extend(donne)
        else:
            self.main.append(donne)
        self.change()

    def choisir(self, options):
        """ choisit aléatoirement parmi les options"""
        return randint(0, len(options)-1) if len(options)> 1 else 0

    def donner_une_carte(self):
        """ retourne une carte qui est retirée de la main du joueur"""
        return self.main.pop(self.choisir(self.main))

    def jouer(self, tapis, jeu):
        """ met une carte sur le tapis en fonction du tapis selon les règles du jeu"""
        # pas de réflexion, pas de suivi des règles du jeu par défaut
        carte = self.donner_une_carte()
        logger.info("{} joue {}".format(self.nom, carte))
        tapis.append((self, carte))
        # pour la surveillance du joueur, signaler un changement
        self.change()
        # pour la surveillance du tapis, signaler un changement
        tapis.change()

class JoueurInteractif(Joueur):
    """Joeur qui prend ses décisions de l'extérieur"""
    # les spécificités de cette classe sont définies dans la vue
    pass


class Carte(object):
    """ Une carte à jouer """
    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur

# pour pouvoir observer les distributions et les prises de cartes
class Pioche(list, Observable):
    """ Une pile de cartes """
    def __init__(self):
        Observable.__init__(self)

# pour pouvoir changer la représentation d'une liste
#et observer les changements sur le tapis
class Tapis(list, Observable):
    """ L'endroit où jouer les cartes """
    def __init__(self):
        Observable.__init__(self)

# pour pouvoir voir les points
class Points(dict, Observable):
    """ L'endroit où inscrire les points et les gagnants """
    def __init__(self):
        Observable.__init__(self)
        self.vider()
        
    def vider(self):
        """ met à blanc toutes les données """
        # les points totaux de la partie
        self.clear()
        # pour mémoriser les points partiels donne par donne
        self.partiels = []
        # pour mémoriser les joueurs gagnant la partie
        self.champions = set()
        # pour savoir quand afficher les gagnants d'une partie
        self.champions_changed = False
        
    
class Table(object):
    """ Lieu de rencontre des joueurs pour jouer"""
    def __init__(self):
       logger.info("Initialisation de la table")
       self.joueurs = []
       self.tapis = Tapis()
       self.pioche = Pioche()
       self.feuille_de_points = Points()

    def accueuillir(self, *joueurs):
        """définit les joueurs de la table"""
        self.joueurs = joueurs

    def dedier(self, jeu):
        """prépare la table à jouer à un jeu donné"""
        self.jeu = jeu
        self.partie = jeu.creer_partie(self.joueurs, self.tapis, self.pioche, self.feuille_de_points)

    def jouer(self):
        """ enchaine les parties tant qu'un joueur interactif le souhaite"""
        self.partie.derouler()

    def veut_arreter(self):
        """retourne vrai si la décision est prise d'arrêter de jouer"""
        # pour l'instant, joue une seule partie du jeu
        # passer de la partie finie à une nouvelle partie sinon
        return True


if __name__=='__main__':
    from jeu import Jeu
    print "début des tests du modèle"
    un_jeu = Jeu()
    print un_jeu.nom
    une_table = Table()
    une_table.dedier(un_jeu)
    print une_table.partie

    un_joueur = Joueur("Testeur")
    print un_joueur.main
    une = 3
    un_joueur.recevoir(une)
    print un_joueur.main
    plusieurs = range(4)
    un_joueur.recevoir(plusieurs)
    print un_joueur.main

    print un_joueur.donner_une_carte()
    print un_joueur.main

