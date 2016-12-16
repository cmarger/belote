#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Outils de support pour un jeu de cartes
Il définit des classes pour mettre en oeuvre le patron observateur-observable
Copyrigth electron-libre de de www.fun-mooc.fr
Licence CeCill v2
novembre 2016
"""

# classe pour le patron observateur-observable
class Event(object):
    pass

class Observable(object):
    def __init__(self):
        self.callbacks = []
    def subscribe(self, callback):
        self.callbacks.append(callback)
    def change(self, **attrs):
        e = Event()
        e.source = self
        for k, v in attrs.iteritems():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)    