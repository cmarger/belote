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
# pas d'import du modèle, même s'il y a une dépendance.

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
        print "Intialisation de la vue"
        # affichage de la table
        def montrer(table):
            vue = ""
            for joueur in table.joueurs:
                vue = vue + repr(joueur) + '\n'
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
            
        def saisir(un_joueur, des_options):
            """permet à un joueur de choisir une carte à donner"""
            # proposer la saisie
            prompt = "Désigner une carte par son numéro d'ordre parmi " + repr(des_options) + " : "
            erreur = "Le numéro saisi doit être entre 1 et " + str(len(des_options))
            while True:
                saisie = raw_input(prompt)
                # convertir la saisie
                numero = int(saisie)
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
        
        # modifier l'affichage d'une carte
        table.partie.pioche[0].__class__.__repr__ = voir_carte
        
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
    une_table = m.Table()
    une_vue=Console(une_table)

    def voir_joueurs(j1,j2):
        print 'j1 = ', repr(j1)
        print 'carte de j1', j1.donner_une_carte()
        print 'j1 = ', repr(j1)
        print 'j2i = ', repr(j2i)
        print 'carte de j2i', j2i.donner_une_carte()
        print 'j2i = ', repr(j2i)               
    
    # Test Joueur
    print "Sans la vue personnalisée ---------------------------"
    j1 = m.Joueur("automatique", True)
    j2i = m.JoueurInteractif("intertactif", True)
    j1.recevoir((m.Carte(0,1), m.Carte(1,7), m.Carte(2,11)))
    j2i.recevoir([m.Carte(2,11), m.Carte(3,13), m.Carte(0,9)])
    print "j1 interactif ?", j1.__class__.__name__
    print "j2i interactif ?", j2i.__class__.__name__
    voir_joueurs(j1, j2i)
    
    une_table.accueuillir(j1, j2i)
    une_table.dedier(m.Jeu())
    une_vue.personnaliser(une_table)
    print "Avec la vue personnalisée ---------------------------"
    carte1 = m.Carte(3, 10)
    carte2 = m.Carte(0,12)
    print "2 cartes = ", carte1, " et ", repr(carte2)

    print repr(une_table)
    voir_joueurs(j1, j2i)
