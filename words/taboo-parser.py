#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import choice
import sqlite3 as dbapi

class Palabras(object):
    def __init__(self, db=':memory:', inicializar=False):
        self._listadoPalabras = []

        self._database = dbapi.connect(db)
        self._cursor = self._database.cursor()

        if (db == ':memory:') or inicializar:
            self._initDB()

    def _initDB(self):
        self._cursor.execute("""
            CREATE TABLE palabras (palabra TEXT PRIMARY KEY,
            taboo01 TEXT, taboo02 TEXT, taboo03 TEXT, taboo04 TEXT,
            taboo05 TEXT)
            """)

        self._database.commit()

    def guardarPalabra(self, palabra):
        try:
            self._cursor.execute("INSERT INTO palabras VALUES (?, ?, ?, ?, ?, ?)",
                (palabra['palabra'], palabra['tabues'][0],
                palabra['tabues'][1], palabra['tabues'][2],
                palabra['tabues'][3],
                palabra['tabues'][4]))

            self._database.commit()
        except dbapi.IntegrityError:
            print "Integrity Error: entrada '%s' repetida..." % (palabra['palabra'], )

    def guardarListado(self):
        for p in self._listadoPalabras:
            self.guardarPalabra(p)

    def leerListado(self):
        self._listadoPalabras = []
        self._cursor.execute("SELECT * FROM palabras")

        for tupla in self._cursor.fetchall():
            palabra = {}
            palabra['palabra'] = tupla[0]
            palabra['tabues'] = []
            for t in range(4):
                palabra['tabues'].append(tupla[t+1])

            self._listadoPalabras.append(palabra)


    def parseFile(self, arch):
        for linea in open(arch):
            palabra = {'tabues' : [], 'palabra' : ''}
            pal = linea.split('\t')
            palabra['palabra'] = unicode(pal[0], 'utf-8')
            for t in pal[1:]:
                palabra['tabues'].append(unicode(t, 'utf-8'))

            self.agregarPalabra(palabra)


    def agregarPalabra(self, p):
        self._listadoPalabras.append(p)


    def mostrarListado(self):
        for p in self._listadoPalabras:
            print p

    def borrarLista(self):
        self._listadoPalabras = []

    def contarPalabras(self):
        return len(self._listadoPalabras)


    def azar(self):
        tarjeta = choice(self._listadoPalabras)
        print 'Palabra: ', tarjeta['palabra']
        print 'Tabues: ',
        print "%s, %s, %s, %s" % tuple(tarjeta['tabues'])


if __name__ == '__main__':

    #pals = Palabras('palabras.db', True)
    pals = Palabras()

    parseFromFile = True

    if parseFromFile:
        pals.parseFile('taboo-words-tabs.txt')

        print 'Tamaño antes de guardar: ', pals.contarPalabras()
        pals.guardarListado()
        print 'Tamaño desp de guardar: ', pals.contarPalabras()
        pals.borrarLista()
        print 'Tamaño desp de borrar: ', pals.contarPalabras()
        pals.mostrarListado()
        pals.leerListado()
        print 'Tamaño desp de leer: ', pals.contarPalabras()
        #pals.azar()

    pals.leerListado()
    print "Hay %d palabras en la db." % (pals.contarPalabras(), )
    pals.azar()
