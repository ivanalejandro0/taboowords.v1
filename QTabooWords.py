#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Ivan Alejandro <ivanalejandro0@yahoo.com.ar>
#
# This file is part of TabooWords.
#
# TabooWords is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TabooWords is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TabooWords.  If not, see <http://www.gnu.org/licenses/>.


from TabooWords import TabooWords

import sys
import os

try:
    from PyQt4 import QtCore, QtGui, uic
except ImportError:
    print "PyQt4 (Qt4 bindings for Python) is required for this application."
    print "You can find it here: http://www.riverbankcomputing.co.uk"
    sys.exit()

from QTemporizador import QTemporizador
from QTabooEdit import QTabooEdit

class QTabooWords(QtGui.QMainWindow, object):
    def __init__ (self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.PalabrasTaboo = TabooWords('palabras.db')

        QtGui.QMainWindow.__init__(self)

        uifile = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'mainWindow.ui')

        uic.loadUi(uifile, self)

        self.ui = self

        msj = "Se han cargado %s palabras." % self.PalabrasTaboo.contarPalabras()
        self.ui.statusbar.showMessage(msj)

        #self.initGUI()
        self.tabooEdit = QTabooEdit()

        self._replaceTemporizador()
        self._setupConnections()
        self._setReglas()
        self.ui.twTarjetasA.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.ui.twTarjetasB.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self._zoomTexto = 0

    def _replaceTemporizador(self):
        oldTiempo = self.ui.lcdTiempo
        self.ui.lcdTiempo = QTemporizador(self.ui.gbTiempo)
        self.ui.gridTiempo.addWidget(self.ui.lcdTiempo, 0, 0, 1, 3)
        oldTiempo.setVisible(False)
        #self.ui.gridTiempo.removeWidget(oldTiempo)

    def _setupConnections(self):
        self.ui.pbSiguiente.clicked.connect(self._on_pbSiguiente_clicked)
        self.ui.pbSumarA.clicked.connect(self._sumarPuntosA)
        self.ui.pbSumarB.clicked.connect(self._sumarPuntosB)
        self.ui.pbGanarA.clicked.connect(self._sumarPuntosA)
        self.ui.pbGanarB.clicked.connect(self._sumarPuntosB)
        self.ui.pbIniciarTiempo.clicked.connect(self.ui.lcdTiempo.iniciar)
        self.ui.pbPausarTiempo.clicked.connect(self.ui.lcdTiempo.pausar)
        self.ui.pbResetearTiempo.clicked.connect(self.ui.lcdTiempo.resetear)
        self.ui.actionInstrucciones.triggered.connect(self._showInstrucciones)
        self.ui.actionAcerca_de.triggered.connect(self._showAbout)
        self.ui.action_Salir.triggered.connect(exit)
        self.ui.vsTextSize.valueChanged.connect(self._on_vsTextSize_valueChanged)
        self.ui.leNombreGrupoA.textEdited.connect(self.tlPuntajeA_2.setText)
        self.ui.leNombreGrupoB.textEdited.connect(self.tlPuntajeB_2.setText)
        self.connect(self.tabooEdit, QtCore.SIGNAL('tabooSaved'), self._saveAndRefresh)

    def _sumarPuntosA(self):
        self.ui.lcdPuntajeA.display(self.ui.lcdPuntajeA.intValue() + 1)
        self.ui.lcdPuntajeA_2.display(self.ui.lcdPuntajeA.intValue())
        self.ui.twTarjetasA.insertRow(0)
        palabra = self.ui.tePalabra.toPlainText().split('\n')[0]
        newItem = QtGui.QTableWidgetItem(palabra)
        self.ui.twTarjetasA.setItem(0, 0, newItem)
        self.ui.pbSumarA.setEnabled(False)
        self.ui.pbSumarB.setEnabled(False)
        self.ui.pbGanarA.setEnabled(False)
        self.ui.pbGanarB.setEnabled(False)

    def _sumarPuntosB(self):
        self.ui.lcdPuntajeB.display(self.ui.lcdPuntajeB.intValue() + 1)
        self.ui.lcdPuntajeB_2.display(self.ui.lcdPuntajeB.intValue())
        self.ui.twTarjetasB.insertRow(0)
        palabra = self.ui.tePalabra.toPlainText().split('\n')[0]
        newItem = QtGui.QTableWidgetItem(palabra)
        self.ui.twTarjetasB.setItem(0, 0, newItem)
        self.ui.pbSumarA.setEnabled(False)
        self.ui.pbSumarB.setEnabled(False)
        self.ui.pbGanarA.setEnabled(False)
        self.ui.pbGanarB.setEnabled(False)

    def _on_pbSiguiente_clicked(self):
        self.currentTaboo = taboo = self.PalabrasTaboo.jugar()

        self._loadTaboo(taboo)

        self.ui.pbSumarA.setEnabled(True)
        self.ui.pbSumarB.setEnabled(True)
        self.ui.pbGanarA.setEnabled(True)
        self.ui.pbGanarB.setEnabled(True)

        self.ui.pbEditarTarjeta.setEnabled(True)

    def _loadTaboo(self, taboo):
        texto = taboo['palabra']

        palabra = '<u>Palabra:</u> <strong>%s</strong><br /><br />\n' % (taboo['palabra'], )
        tabues = '<u>Tabues:</u>\n<em><ul>\n'

        for t in taboo['tabues']:
            tabues = tabues + '<li>' + t + '</li>\n'
        tabues = tabues + '</ul></em>\n'

        texto = '<h3>%s%s</h3>' % (palabra, tabues)

        self.ui.tePalabra.setHtml(texto)

    def _saveAndRefresh(self, oldT, palabra):
        self.PalabrasTaboo.updatePalabra(oldT, palabra)
        self._loadTaboo(palabra)

    @QtCore.pyqtSlot()
    def on_pbEditarTarjeta_clicked(self):
        self.tabooEdit.load_taboo(self.currentTaboo)
        self.tabooEdit.show()

    def _on_vsTextSize_valueChanged(self, i):
        if self._zoomTexto < i:
            self.ui.tePalabra.zoomIn()
        else:
            self.ui.tePalabra.zoomOut()

        self._zoomTexto = i

    def _setReglas(self):
        self.reglas = """<big>
            <center><strong>REGLAS DEL JUEGO</strong></center><br />
            <strong>N&uacute;mero de jugadores:</strong> De 4 a 30.<br />
            <strong>Edad de los jugadores:</strong> A partir de los 12 a&ntilde;os.<br />
            <strong>Duraci&oacute;n:</strong> El que se establezca o el que llega antes a un numero determinado de tarjetas.<br />
            <br /><br />
            <strong><u>Como Jugar:</u></strong>
            <ol>
            <li>Se dividen las personas en 2 equipos.</li>
            <li>Cada equipo tiene un turno y 60 segundos para hacerse entender.</li>
            <li>La persona elegida por el equipo de turno tiene que intentar hacerle a entender a sus compa&ntilde;eros la palabra dada como consigna en MAYUSCULAS sin decir las 5 palabras dadas como tab&uacute;es.</li>
            <li>Del equipo contrario tiene que haber una persona controlando que al parafrasear no se diga ninguna las palabras prohibidas. (como restricci&oacute;n adicional se puede prohibir usar las palabras similares o de la misma familia que las de la tarjeta)</li>
            <li>Si se adivina la palabra consigna en el tiempo dado el equipo gana la tarjeta, sino la gana el equipo contrario.</li>
            </ol>
            </big>
            """
        msj = self.tr("Para instrucciones debe ir al menu\nAyuda->Como jugar?.")
        self.ui.tePalabra.setHtml(msj)

    def _showInstrucciones(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(self.reglas)
        msgBox.exec_()

    def _showAbout(self):
        msgBox = QtGui.QMessageBox()
        self.about = """<center><strong>TabooWords</strong</center><br />\n
            Versi&oacute;n inform&aacute;tica del juego de tablero en grupos en el cual se debe explicar una palabra a tus compa&ntilde;eros sin usar las palabras dadas como taboo.<br /><br />\n
            Autor: Ivan Alejandro &lt;ivanalejandro0@yahoo.com.ar&gt;
            """
        msgBox.setText(self.about)
        msgBox.exec_()



def main():
    app = QtGui.QApplication(sys.argv)
    prog = QTabooWords()
    prog.show()
    app.exec_()

    return 0


if __name__ == "__main__":
    main()
