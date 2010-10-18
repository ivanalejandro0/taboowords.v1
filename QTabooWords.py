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

from TabooWords import TabooWords
from mainWindow import Ui_MainWindow

import sys

try:
    #from PyQt4 import QtCore
    from PyQt4 import QtGui
except ImportError:
    print "PyQt4 (Qt4 bindings for Python) is required for this application."
    print "You can find it here: http://www.riverbankcomputing.co.uk"
    sys.exit()

from QTemporizador import QTemporizador

class QTabooWords(QtGui.QMainWindow, object):
    def __init__ (self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.PalabrasTaboo = TabooWords('palabras.db')

        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)

        msj = "Se han cargado %s palabras." % self.PalabrasTaboo.contarPalabras()
        self.UI.statusbar.showMessage(msj)

        #self.initGUI()

        self._replaceTemporizador()
        self._setupConnections()
        self._setReglas()
        self.UI.twTarjetasA.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.UI.twTarjetasB.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self._zoomTexto = 0


    def _replaceTemporizador(self):
        oldTiempo = self.UI.lcdTiempo
        self.UI.lcdTiempo = QTemporizador(self.UI.gbTiempo)
        self.UI.gridTiempo.addWidget(self.UI.lcdTiempo, 0, 0, 1, 3)
        oldTiempo.setVisible(False)
        #self.UI.gridTiempo.removeWidget(oldTiempo)


    def _setupConnections(self):
        self.UI.pbSiguiente.clicked.connect(self._on_pbSiguiente_clicked)
        self.UI.pbSumarA.clicked.connect(self._sumarPuntosA)
        self.UI.pbSumarB.clicked.connect(self._sumarPuntosB)
        self.UI.pbIniciarTiempo.clicked.connect(self.UI.lcdTiempo.iniciar)
        self.UI.pbPausarTiempo.clicked.connect(self.UI.lcdTiempo.pausar)
        self.UI.pbResetearTiempo.clicked.connect(self.UI.lcdTiempo.resetear)
        self.UI.actionInstrucciones.triggered.connect(self._showInstrucciones)
        self.UI.vsTextSize.valueChanged.connect(self._on_vsTextSize_valueChanged)



    def _sumarPuntosA(self):
        self.UI.lcdPuntajeA.display(self.UI.lcdPuntajeA.intValue() + 1)
        self.UI.twTarjetasA.insertRow(0)
        palabra = self.UI.tePalabra.toPlainText().split('\n')[0]
        newItem = QtGui.QTableWidgetItem(palabra)
        self.UI.twTarjetasA.setItem(0, 0, newItem)
        self.UI.pbSumarA.setEnabled(False)
        self.UI.pbSumarB.setEnabled(False)



    def _sumarPuntosB(self):
        self.UI.lcdPuntajeB.display(self.UI.lcdPuntajeB.intValue() + 1)
        self.UI.twTarjetasB.insertRow(0)
        palabra = self.UI.tePalabra.toPlainText().split('\n')[0]
        newItem = QtGui.QTableWidgetItem(palabra)
        self.UI.twTarjetasB.setItem(0, 0, newItem)
        self.UI.pbSumarA.setEnabled(False)
        self.UI.pbSumarB.setEnabled(False)


    def _on_pbSiguiente_clicked(self):
        taboo = self.PalabrasTaboo.jugar()
        texto = taboo['palabra']

        palabra = '<u>Palabra:</u> <strong>%s</strong><br /><br />\n' % (taboo['palabra'], )
        tabues = '<u>Tabues:</u>\n<em><ul>\n'

        for t in taboo['tabues']:
            tabues = tabues + '<li>' + t + '</li>\n'

        tabues = tabues + '</ul></em>\n'

        texto = '<h3>%s%s</h3>' % (palabra, tabues)

        print texto

        self.UI.tePalabra.setHtml(texto)
        self.UI.pbSumarA.setEnabled(True)
        self.UI.pbSumarB.setEnabled(True)


    def _on_vsTextSize_valueChanged(self, i):
        if self._zoomTexto < i:
            self.UI.tePalabra.zoomIn()
        else:
            self.UI.tePalabra.zoomOut()

        self._zoomTexto = i


    def _setReglas(self):
        self.reglas = """<big>
            <center><strong>REGLAS DEL JUEGO</strong></center><br />
            <strong>N&uacute;mero de jugadores:</strong> De 6 a 30.<br />
            <strong>Edad de los jugadores:</strong> A partir de los 12 a&#241;os.<br />
            <strong>Duraci&oacute;n:</strong> El que se establesca, pero es mejor el que llegua a un numero determinado de tarjetas.<br />
            <strong>Meta del juego:</strong> El equipo que adivine m&#225;s palabras en un tiempo preestablecido, gana m&#225;s tarjetas. El que tenga m&#225;s tarjetas al final del juego, ser&#225; el ganador.<br />
            <strong>Material requerido</strong>: tarjetas, cada una con una palabra por definir y cuatro palabras prohibidas.<br />

            <br /><br />
            <strong><u>Como Jugar:</u></strong>
            <ol>
            <li>Organizar al total de jugadores en dos equipos. En grupos mayores a 15 , puede ser recomendable hacer tres o m&#225;s equipos.</li>
            <li>Pedir que cada equipo elija un representante.</li>
            <li>El representante del primer equipo pasa al frente, con 5 tarjetas. Un miembro del segundo equipo se para junto a &eacute;l para:</li>
            <ul>
            <li>Vigilar que no use ninguna de las palabras prohibidas al definir la palabra que le toc&oacute;.</li>
            <li>Medir el tiempo. Cada equipo tendr&aacute; un minuto para descubrir la(s) palabra(s) que su representante defina.</li>
            </ul>
            <li>El representante del primer equipo tiene un minuto para parafrasear la palabra que aparece en may&#250;sculas en la parte superior de cada tarjeta, pero NO podr&#225; usar ninguna de las palabras incluidas en la misma tarjeta porque son tab&#250;.</li>
            <li>El equipo tratar&#225; de adivinar la palabra. Si lo logra, obtendr&#225; esa tarjeta y el representante parafrasear&#225; la tarjeta siguiente. Continuar as&#237; hasta que termine su tiempo.</li>
            <li>Al terminar el tiempo de un equipo continuar&#225; el otro siguiendo las mismas reglas.</li>
            </ol>
            </big>
            """
        msj = self.tr("Para instrucciones debe ir al menu\nAyuda->Como jugar?.")
        self.UI.tePalabra.setHtml(msj)


    def _showInstrucciones(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(self.reglas)
        msgBox.exec_()



def main():
    app = QtGui.QApplication(sys.argv)
    prog = QTabooWords()
    prog.show()
    app.exec_()

    return 0


if __name__ == "__main__":
    main()
