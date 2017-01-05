#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contrôleur d'un jeu de cartes
Jeu de cartes construit sur le principe de Modèle-Vue-Contrôleur.
Les 3 parties M, V et C sont chacune dans un module.
Le contrôleur utilise la vue et le modèle.
Le contrôleur est le module qui doit être lancé pour démarrer le jeu.
Copyrigth electron-libre de www.fun-mooc.fr
Licence CeCill v2
novembre 2016
"""

# module logger
import logging
logging.basicConfig(filename='belote.log',level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("controleur")

# les 2 autres modules sont importés pour être utilisés.
import modele as m
import vue as v
from jeu import Jeu


class Controleur(object):
    """
    Le controleur crée les objets utilisés
    à partir des classes des modules de la vue et du modèle.
    """
    def __init__(self, vue = 'C'):
        """crée les données du controleur et la vue sur ces données"""
        self.table = m.Table()
        if vue == 'G':
            self.vue = v.Graphique(self.table)
        else:
            self.vue = v.Console(self.table)

    def personnaliser(self):
        """met en place les joueurs et le jeu"""
        logger.info("Démarrage du contrôleur")

        # détermine les joueurs interactifs
        # pour commencer un seul
        moi = m.JoueurInteractif("moi", visible = True)

        # installe les joueurs à la table
        # pour commencer par programme
        self.table.accueuillir(moi, m.Joueur("gauche"), m.Joueur("partenaire"), m.Joueur("droite"))

        # prepare la table pour un jeu de cartes
        # pour commencer un jeu générique
        self.table.dedier(Jeu())
        self.vue.personnaliser(self.table)
        self.vue.afficher()

    def activer(self):
        """démarre le jeu et le poursuit jusqu'à la fin"""
        logger.info("Déroulement du jeu")
        while True:
            self.table.jouer()
            if self.table.veut_arreter():
                break
            else:
                continue

def animer(table_de_jeu):
    table_de_jeu = Controleur()
    table_de_jeu.personnaliser()
    table_de_jeu.activer()

if __name__=='__main__':
    # la variable table est globale pour qu'elle soit visible pendant
    # l'execution par le debogueur,
    # elle pourra ainsi faciliter la mise au point
    logger.info("Lancement Belote")
    table_de_jeu = None
    animer(table_de_jeu)
