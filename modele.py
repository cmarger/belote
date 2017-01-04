#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modèle d'un jeu de cartes
Jeu de cartes construit sur le principe de Modèle-Vue-Contrôleur.
Ce module est celui du modèle.
Son interface est utilisée par le contrôleur uniquement.
Son contenu est connu et en partie modifié par la vue.
Il ne connaît rien du contrôleur ni de la vue.
Il définit les classes et leurs interactions nécessaires au jeu.
Copyrigth electron-libre de de www.fun-mooc.fr
Licence CeCill v2
novembre 2016
"""
# utilisé quand il faut prendre une décision "au pif"
from random import randint, shuffle
# utilisé pour surveiller le tapis
from support import Observable
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
    def __init__(self):
        Observable.__init__(self)
        # pour mémoriser les points donne par donne
        self.partiels = []
        # pour mémoriser les joueurs en tête, en cours et en fin de partie
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

class Jeu(object):
    """ Jeu de cartes """
    def __init__(self, nom = "Basique", nb_cartes = 32):
        self.nom = nom
        self.nb_cartes = nb_cartes
        # nombre maximal de donne par défaut pour finir la partie
        self.nb_max_donnes = 2
        # nombre maximal de points par défaut pour finir la partie
        self.nb_max_points = 1000

        # ensemble de cartes utilisées
        def generateur_cartes():
            couleurs = range(4)
            # les valeurs sont en rapport avec les chiffres des cartes
            # les points associés à ces valeurs dépendent du jeu
            temp = range(14)
            if nb_cartes == 32:
                valeurs = temp[1:2] + temp[7:]
            else:
                valeurs = temp[1:]
            """generateur de jeu de cartes"""
            for couleur in couleurs:
                for valeur in valeurs:
                    carte = Carte(couleur, valeur)
                    yield carte
        # ! attribut du jeu qui est une fonction génératrice,
        # et non une méthode de la classe
        self.creer_cartes = generateur_cartes

        # définition des étapes d'une partie
        def battre(une_partie):
            """ bat les cartes à distribuer"""
            logger.info("Jeu mélangé")
            shuffle(une_partie.pioche)

        def distribuer(une_partie):
            """ distribution de toutes les cartes aux joueurs"""
            # par défaut toutes les cartes
            while len(une_partie.pioche):
                for joueur in une_partie.joueurs:
                    joueur.recevoir(une_partie.pioche.pop())

        def jouer(une_partie):
            """ joue la partie """
            nb_plis = nb_cartes / len(une_partie.joueurs)
            while len(une_partie.plis) < nb_plis:
                for joueur in une_partie.joueurs:
                    joueur.jouer(une_partie.tapis, une_partie.jeu)
                # pour compter les poins à la fin, copie nécessaire
                une_partie.plis.append([coup for coup in une_partie.tapis])
                # vider le tapis existant et non le réinitialiser vide
                del une_partie.tapis[0:]
                # pour surveiller le tapis, signale un changement
                une_partie.tapis.change()

        def compter(une_donne):
            """ compter les points """
            # par défaut, même points pour chaque joueur
            for joueur in une_donne.joueurs:
                une_donne.scores[joueur] = 100

        # definition du processus de déroulement d'un donne
        self.plan_donne = (battre, distribuer, jouer, compter)
                
    def creer_partie(self, joueurs, tapis, pioche, feuille_de_points):
        """ 
        Initialise le jeu avec les éléments du contexte passés en paramètres
        Retourne un objet (de type Partie) qui supporte la méthode derouler()
        """
        return Partie(self, joueurs, tapis, pioche, feuille_de_points)

class Partie(object):
    """ Partie de cartes """
    def __init__(self, jeu, joueurs, tapis, pioche, feuille_de_points):
        self.jeu = jeu
        # mémoriser les données nécessaires à une donne pour créer les suivantes
        self.joueurs = joueurs
        self.tapis = tapis
        self.pioche = pioche
        self.feuille_de_points = feuille_de_points
        # prépare la première la donne à être jouée
        self.donne_en_cours = Donne(self.jeu, self.joueurs, self.tapis, self.pioche)
        # toutes les donnes jouées de la partie
        self.donnes = []
        
    # pour qu'une partie puisse enchaîner plusieurs donnes
    def derouler(self):
        """ enchaine les donnes jusqu'à la fin du jeu """
        nb_donnes = 0
        self.feuille_de_points.clear()
        while True:
            self.donne_en_cours.derouler()
            nb_donnes = nb_donnes + 1
            # cumule les points de chaque donne 
            # conserve les donnes jouées en mémoire pour plus tard
            self.cumuler(self.donne_en_cours)
            self.feuille_de_points.change()
            # déterminer la fin la jeu selon la règle ad hoc
            if self.est_finie(self.feuille_de_points, nb_donnes):
                # détermine les gagnants
                self.proclamer()
                self.feuille_de_points.change()
                # mémorise l'ensemble des donnes jouées (plus tard)
                break
            else:
                # continuer la partie avec une nouvelle donne
                self.donne_en_cours = Donne(self.jeu, self.joueurs, self.tapis, self.pioche)
                continue

    def cumuler(self, une_donne):
        """ 
        cumuler les points d'une donne dans le résultat de la partie
        par addition des points pour chaque joueur
        """
        self.donnes.append(une_donne)
        self.feuille_de_points.partiels.append(une_donne.scores)
        if self.feuille_de_points:
            for joueur, points in une_donne.scores.iteritems():
                self.feuille_de_points[joueur] = \
                self.feuille_de_points[joueur] + points
        else:
            for joueur, points in une_donne.scores.iteritems():
                self.feuille_de_points[joueur] = points
                    
    def proclamer(self):
        """ déterminer le ou les gagnants selon la feuille de points """
        # par défaut, celui qui a le nombre de points le plus grand
        max = 0
        self.feuille_de_points.champions = set()
        for joueur, points in self.feuille_de_points.iteritems():
            # pour accepter les ex-eaquo, il faut aussi l'égalité
            if points >= max:
                max = points
                self.feuille_de_points.champions.add(joueur)
        self.feuille_de_points.champions_changed = True

    def est_finie(self, des_points, nb_donnes = 0):
        """ 
        retourne True pour finir la partie, False pour continuer
        selon les points accumulés ou le nombre de donnes  
        """
        decision = False
        # critère du nombre de donnes
        if self.jeu.nb_max_donnes:
            if nb_donnes >= self.jeu.nb_max_donnes:
                decision = True
        elif self.jeu.nb_max_points:
            # critère du nombre de points    
            for joueur, points in self.feuille_de_points.iteritems():
                if points >= self.jeu.nb_max_points:
                    decision = True
                    break
        else:
            # il manque la définition pour au moins un des 2 critères
            logger.error("nb max de point = {} et nb max donnes ={}"\
            .format(self.jeu.nb_max_points, self.jeu.nb_max_donnes))
            # par précaution, la partie d'arrête pour éviter la boucle infinie
            decision = True
        return decision    
                
                
class Donne(object):
    """ Donne d'une partie de cartes """
    def __init__(self, jeu, joueurs, tapis, pioche):
        self.jeu = jeu
        self.pioche = pioche
        self.pioche.extend([cartes for cartes in jeu.creer_cartes()])
        self.joueurs = joueurs
        self.tapis = tapis
        self.plan = jeu.plan_donne
        self.plis = []
        self.scores = {}

    def derouler(self):
        for etapes in self.plan:
            etapes(self)



if __name__=='__main__':
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

    # tests d'une donne, etape par etape
    print "tests d'une donne, etape par etape"
    def print_donne(une_donne):
        print 'Affichage de la donne :---------'
        print 'pioche = ', une_donne.pioche, len(une_donne.pioche)
        print 'joueurs = ', [j.main for j in une_donne.joueurs]
        print 'tapis = ', une_donne.tapis, len(une_donne.tapis)
        print 'scores = ', une_donne.scores
        print 'plis = ', une_donne.plis, len(une_donne.plis)
        print 'process =', une_donne.plan
        print "--------------------------------- "

    une_table = Table()
    une_table.accueuillir(Joueur("un"), Joueur("deux"), Joueur("trois"), Joueur("quatre"))
    une_donne = Donne(un_jeu, une_table.joueurs, une_table.tapis, une_table.pioche)

    print_donne(une_donne)
    for pas in une_donne.plan:
        print '===> ', pas.__name__
        pas(une_donne)
        print_donne(une_donne)


    #test d'une partie
    print "tests d'une partie"
    def print_partie(une_partie):
        print 'Affichage de la partie :---------'
        print 'joueurs = ', [j.main for j in une_partie.joueurs]
        print 'pioche = ', une_partie.pioche, len(une_partie.pioche)
        print 'tapis = ', une_partie.tapis
        print 'points = ', une_partie.feuille_de_points
        print 'donnes = ', une_partie.donnes, len(une_partie.donnes)
        print "--------------------------------- "

    une_table = Table()
    print une_table.__dict__
    une_table.accueuillir(Joueur("un"), Joueur("deux"), Joueur("trois"), Joueur("quatre"))
    une_partie = un_jeu.creer_partie(
        une_table.joueurs, une_table.tapis, une_table.pioche, une_table.feuille_de_points)
    # enchainement
    print_partie(une_partie)
    print "Deroulement de la partie"
    une_partie.derouler()
    print_partie(une_partie)

    #test d'un jeu
    print "Deroulement d'un jeu fils"
    class Jeu_test(Jeu):
        def __init__(self):
            Jeu.__init__(self)
            self.nb_max_donnes = 3
    
    un_jeu = Jeu_test()
    print un_jeu.nb_max_donnes
    une_table = Table()
    une_table.accueuillir(Joueur("un"), Joueur("deux"), Joueur("trois"), Joueur("quatre"))
    une_table.dedier(un_jeu)

    une_partie = un_jeu.creer_partie(
        une_table.joueurs, une_table.tapis, une_table.pioche, une_table.feuille_de_points)
    une_partie.derouler()
    print_partie(une_partie)
