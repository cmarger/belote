#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vue d'un jeu de cartes
Jeu de cartes construit sur le principe de Modèle-Vue-Contrôleur.
Ce module est celui de la vue.
Son interface est utilisée par le contrôleur uniquement.
Il ne connaît rien du contrôleur.
Il connait les classes du modèle.
Il utilise les objets qui lui sont passés en argument pour modifier le modèle.
Copyrigth electron-libre de de www.fun-mooc.fr
Licence CeCill v2
novembre 2016
"""
import logging
logger = logging.getLogger("vue")
# pas d'import du modèle, même s'il y a une dépendance.
# expressions régulières pour le contrôle de la saisie
import re


class Vue(object):
    #pour mettre en commun les traitements communs des vues
    pass

class Console(Vue):
    """ Affiche dans un terminal en mode caractère """
    def __init__(self, modele):
        """
        Mémorise l'objet à afficher : la table et
        Définit les façons de l'afficher ainsi que ses composants
        """
        self.modele = modele

        # nombre de caractères en largeur et ligne en hauteur
        self.largeur = 80

        logger.info("Intialisation de la vue")
        
        # affichage du tapis
        def voir_tapis(un_tapis):
            # mise en forme en colonnes, un coup par ligne
            vue = self.largeur*'-'
            # en dur la marge, arbitraire
            # mise en forme pour la carte puis le nom du jou[eur
            ligne = (self.largeur / 3 - self.l_max_carte)*' ' \
                    + "{carte:<" + str(self.l_max_carte) + "} {nom}\n"
            for coup in un_tapis:
                vue = vue \
                      + ligne.format(carte = repr(coup[1]), nom = coup[0].nom)
            vue = vue + self.largeur*'.'
            return vue
        self.modele.tapis.__class__.__repr__ = voir_tapis
        # mettre en place la surveillance du tapis
        def surveiller(un_event):
            print repr(un_event.source)
        # en utilisant le fait que c'est un Observable
        self.modele.tapis.subscribe(surveiller)

        # affichage des points
        # largeur prévue pour un jeu en 1000 points
        self.l_max_points = 5
        def voir_points(une_feuille):
            # mise en forme en colonnes, un coup par ligne
            vue = self.largeur*'*'
            
            # après que les gagnants ont été proclamés, ils sont affichés 
            if une_feuille.champions_changed:
                # en dur la marge, arbitraire
                # mise en forme pour les totaux de points puis le nom du joueur
                ligne = (self.largeur / 3 - self.l_max_points)*' ' \
                    + "{valeur:<" + str(self.l_max_points) + "} {nom}\n"
                for joueur, points in une_feuille.iteritems():
                    vue = vue \
                      + ligne.format(valeur = repr(points), nom = joueur.nom)
                # les gagnants
                vue = vue + \
                      "Les gagnants de la partie sont :".center(self.largeur) +\
                      "\n"
                vue = vue + \
                      str([champion.nom for champion in une_feuille.champions]).\
                      center(self.largeur)
            else:
                # après chaque donne, les totaux sont affichés,
                # le détail des points de chaque donne devrait l'être aussi
                # en tableau : colonne = joueur, ligne = donne,
                # mise en forme pour les totaux de points puis le nom du joueur
                ligne = (self.largeur / 3 - self.l_max_points)*' ' \
                    + "{valeur:<" + str(self.l_max_points) + "} {nom}\n"
                for joueur, points in une_feuille.iteritems():
                    vue = vue \
                      + ligne.format(valeur = repr(points), nom = joueur.nom)
                
            vue = vue + self.largeur*'*'
            return vue
        self.modele.feuille_de_points.__class__.__repr__ = voir_points

        # mettre en place la surveillance de la feuille
        self.modele.feuille_de_points.subscribe(surveiller)
        
        # affichage de la table
        def montrer(table):
            vue = ""
            for joueur in table.joueurs:
                vue = vue + repr(joueur) + '\n'
            vue = vue + repr(table.tapis)
            vue = vue + repr(table.feuille_de_points)
            return vue    
        self.modele.__class__.__repr__ = montrer

    def personnaliser(self, table):
        """rend un joueur capable d'interagir via la vue"""
        # séparé de l'initialisation pour tenir compte des joueurs interactifs

        # affichage d'un joueur
        def montrer(joueur):
            vue = "\t\t"
            for c in joueur.main:
                # affichage d'une carte selon qu'elle est de dos ou de face
                vue = vue + " " + (repr(c) if joueur.visible else "X")
            vue = vue + "\t" + joueur.nom
            return vue

        # Expression régulière qui contraint la saisie
        self.format_saisie = re.compile("^[1-8]\Z")
        def saisir(un_joueur, des_options):
            """permet à un joueur de choisir une carte à donner"""
            # proposer la saisie
            max = str(len(des_options))
            prompt = "Désigner une carte parmi " + repr(des_options) + \
                     " \npar son numéro d'ordre de 1 à " + max + " : "
            erreur = "Le numéro saisi doit être entre 1 et " + max
            while True:
                saisie = raw_input(prompt)
                # convertir la saisie
                verif = (self.format_saisie).match(saisie)
                if verif:
                    numero = int(saisie)                    
                else:
                    print erreur
                    continue
                # tester la validité de la saisie
                if numero <= len(des_options) and numero > 0:
                    break
                else:
                    print erreur
                    continue
            # retourner l'index de l'option choisie
            return numero-1

        # modifier le comportement du joueur d'automatique à interactif
        for joueur in table.joueurs:
            joueur.__class__.__repr__ = montrer
            if joueur.__class__.__name__ == 'JoueurInteractif':
                # modifie la façon de décider d'un joueur
                joueur.__class__.choisir = saisir

        couleurs = ('Ca', 'Pi', 'Co', 'Tr')
        valeurs = ('V', 'D', 'R')
        # affichage d'une carte
        def voir_carte(une_carte):
            """permet de voir une carte"""
            vue = couleurs[une_carte.couleur] + '-'
            vue = vue + (str(une_carte.valeur) if une_carte.valeur < 11 else valeurs[une_carte.valeur - 11])
            return vue
        # longueur maximale de l'affichage d'une carte incluant les ()
        self.l_max_carte = 7

        # modifier l'affichage d'une carte
        # contraint l'existence d'au moins une carte dans la pioche
        table.pioche[0].__class__.__repr__ = voir_carte

    def afficher(self):
        """ affiche l'état courant d'ensemble"""
        print repr(self.modele)        

class Graphique(Vue):
    """ affiche en mode graphique"""
    # utiliser la bibliothèque PyGame spécialisée , sinon tkinter ou PyQt
    pass

# pour des tests propres au module
if __name__=='__main__':
    import modele as m
    from jeu import Jeu
    une_table = m.Table()
    une_vue=Console(une_table)

    def animer_joueurs(j1,j2):
        print " animation de 2 joueurs ........... "
        print "2 joueurs :\n"
        print 'j1 avant = ', repr(j1)
        print 'carte choisie par j1 :', j1.donner_une_carte()
        print 'j1 ensuite = ', repr(j1)
        print 'j2i avant = ', repr(j2i)
        c =  j2i.donner_une_carte()
        print 'carte choisie par j2i :', c
        print 'j2i ensuite = ', repr(j2i)               
        print " animation de 2 joueurs ........... fin"

    # Test carte
    carte1 = m.Carte(3, 10)
    carte2 = m.Carte(0,12)
    print "2 cartes = ", carte1, " et ", repr(carte2)

    # Test Joueur
    j1 = m.Joueur("automatique", True)
    j2i = m.JoueurInteractif("intertactif", True)
    j1.recevoir((m.Carte(0,10), m.Carte(1,10), m.Carte(2,10)))
    j2i.recevoir([m.Carte(2,12), m.Carte(3,13), m.Carte(0,9)])
    print "j1 interactif ?", j1.__class__.__name__
    print "j2i interactif ?", j2i.__class__.__name__
    print "Sans la vue personnalisée ---------------------------"
    animer_joueurs(j1, j2i)

    print "Avec la vue personnalisée ---------------------------"
    une_table.accueuillir(j1, j2i)
    un_jeu = Jeu()
    une_table.dedier(un_jeu)
    une_vue.personnaliser(une_table)
    print repr(une_table)
    animer_joueurs(j1, j2i)
    
    # Test tapis
    j1.jouer(une_table.tapis, un_jeu)
    j2i.jouer(une_table.tapis, un_jeu)
    print repr(une_table)
    
    
