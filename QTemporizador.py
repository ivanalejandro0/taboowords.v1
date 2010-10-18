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
try:
    from PyQt4 import QtCore
    from PyQt4 import QtGui
except ImportError:
    print "PyQt4 (Qt4 bindings for Python) is required for this application."
    print "You can find it here: http://www.riverbankcomputing.co.uk"
    sys.exit()


class QTemporizador(QtGui.QLCDNumber):
    def __init__(self, parent=None):
        QtGui.QLCDNumber.__init__(self, parent)

        self.setNumDigits(3)
        self.setSegmentStyle(QtGui.QLCDNumber.Filled)

        self._tiempo = QtCore.QTimer()
        self.display( 60 )
        self._tiempo.timeout.connect(self._decrementar)


    def iniciar(self):
        self._tiempo.start(1000)


    def pausar(self):
        self._tiempo.stop()


    def resetear(self):
        self._tiempoNegro()
        self.display( 60 )
        self._tiempo.stop()


    def _decrementar(self):
        anterior = self.intValue()
        if anterior > 0:
            self.display( anterior - 1)
            if anterior == 11:
                self._tiempoRojo()
        else:
            self._tiempo.stop()


    def _tiempoRojo(self):
        self.setSegmentStyle(QtGui.QLCDNumber.Filled);
        paleta = self.palette()
        paleta.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        #paleta.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(paleta)


    def _tiempoNegro(self):
        self.setSegmentStyle(QtGui.QLCDNumber.Filled);
        paleta = self.palette()
        paleta.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)
        #paleta.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(paleta)

if __name__ == '__main__':
	pass

