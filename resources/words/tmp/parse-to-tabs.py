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



if __name__ == '__main__':
    print "Comienzo"
    linea = []
    descartados = []
    palabras = []
    mal = []

    for p in open('taboo-words.txt'):
        if p.strip() not in ('\xc3\xa7', '\xc2\xa0', ''):
            if len(linea) == 6:
                #print linea
                if linea[0].upper() != linea[0]:
                    mal.append(len(palabras))
                    mal.append(linea)
                palabras.append(linea)
                linea = []
            linea.append(p.strip())
        else:
            descartados.append(p)

t = {}
for k in descartados:
    t[k] = 1

descartados = []

for k in t.keys():
    descartados.append(k)

print descartados

arch = open('taboo-words-tabs.txt', 'w')
for pal in palabras:
    for p in pal:
        arch.write(p)
        if p != pal[-1]:
            arch.write('\t')
    arch.write('\n')

arch.close()
