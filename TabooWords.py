#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#
#       Copyright 2010 Ivan Alejandro <ivan@sabagentoo>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from random import choice
import sqlite3 as dbapi

class TabooWords(object):
    def __init__(self, db=':memory:', inicializar=False):
        self._listadoPalabras = []

        self._palabrasJugadas = []

        self._database = dbapi.connect(db)
        self._cursor = self._database.cursor()

        if (db == ':memory:') or inicializar:
            self._initDB()
        else:
            self._loadDB()


    def __del__(self):
        self._cursor.close()
        self._database.close()


    def _initDB(self):
        self._cursor.execute("""
            CREATE TABLE palabras (palabra TEXT PRIMARY KEY,
            taboo01 TEXT, taboo02 TEXT, taboo03 TEXT, taboo04 TEXT,
            taboo05 TEXT)
            """)

        self._database.commit()


    def _loadDB(self):
        self._listadoPalabras = []
        self._cursor.execute("SELECT * FROM palabras")

        for tupla in self._cursor.fetchall():
            palabra = {}
            palabra['palabra'] = tupla[0]
            palabra['tabues'] = []
            for t in range(5):
                palabra['tabues'].append(tupla[t+1])

            self._listadoPalabras.append(palabra)


    def guardarPalabra(self, palabra):
        try:
            self._cursor.execute("INSERT INTO palabras VALUES (?, ?, ?, ?, ?, ?)",
                (palabra['palabra'], palabra['tabues'][0],
                palabra['tabues'][1], palabra['tabues'][2],
                palabra['tabues'][3], palabra['tabues'][4]))

            self._database.commit()
        except dbapi.IntegrityError:
            print "Integrity Error: entrada '%s' repetida..." % (palabra['palabra'], )

    def _updatePalabra(self, old, palabra):
        print "updatePalabra:"
        print "Old: %s\nNew: %s" % (old, palabra)

    def updatePalabra(self, old, palabra):
        self._updatePalabra(old, palabra)
        self._cursor.execute("""UPDATE palabras SET palabra=?,
            taboo01=?, taboo02=?, taboo03=?, taboo04=?, taboo05=?
            WHERE palabra=?""",
            (palabra['palabra'], palabra['tabues'][0],
            palabra['tabues'][1], palabra['tabues'][2],
            palabra['tabues'][3], palabra['tabues'][4],
            old['palabra'])
            )

        self._database.commit()

    def saveOrUpdate(self, palabra):
        try:
            self._cursor.execute("INSERT INTO palabras VALUES (?, ?, ?, ?, ?, ?)",
                (palabra['palabra'], palabra['tabues'][0],
                palabra['tabues'][1], palabra['tabues'][2],
                palabra['tabues'][3], palabra['tabues'][4]))
        # si el codigo ya existe -> actualizo
        except dbapi.IntegrityError:
            self._cursor.execute("""UPDATE palabras SET palabra=?,
                taboo01=?, taboo02=?, taboo03=?, taboo04=?, taboo05=?
                WHERE palabra=?""",
                (palabra['palabra'], palabra['tabues'][0],
                palabra['tabues'][1], palabra['tabues'][2],
                palabra['tabues'][3], palabra['tabues'][4],
                palabra['palabra'])
                )

        self._database.commit()


    def guardarListado(self):
        for p in self._listadoPalabras:
            #self.guardarPalabra(p)
            self.saveOrUpdate(p)


    def agregarPalabra(self, p):
        self._listadoPalabras.append(p)


    def mostrarListado(self):
        for p in self._listadoPalabras:
            print p


    def borrarListado(self):
        self._listadoPalabras = []


    def contarPalabras(self):
        return len(self._listadoPalabras)


    def jugar(self, mostrar=False):
        tarjeta = choice(self._listadoPalabras)

        while tarjeta in self._palabrasJugadas:
            tarjeta = choice(self._listadoPalabras)

        self._palabrasJugadas.append(tarjeta)

        if mostrar:
            print 'Palabra: ', tarjeta['palabra']
            print 'Tabues: ',
            print "%s, %s, %s, %s, %s" % tuple(tarjeta['tabues'])
        else:
            return tarjeta


def main():
    palabras = TabooWords('palabras.db')
    print "Se cargaron %d palabras." % (palabras.contarPalabras(), )
    palabras.jugar(True)
    #palabras.guardarListado()


if __name__ == '__main__':
    main()

