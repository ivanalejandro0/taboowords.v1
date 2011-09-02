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

import sys, os

try:
    from PyQt4 import QtCore, QtGui, uic
except ImportError:
    print "PyQt4 (Qt4 bindings for Python) is required for this application."
    print "You can find it here: http://www.riverbankcomputing.co.uk"
    sys.exit()


class QTabooEdit(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        uifile = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'tabooEdit.ui')

        uic.loadUi(uifile, self)
        self.ui = self

    def load_taboo(self, taboo):
        self.editedTaboo = taboo
        self.ui.lePalabra.setText(taboo['palabra'])
        self.ui.leTaboo1.setText(taboo['tabues'][0])
        self.ui.leTaboo2.setText(taboo['tabues'][1])
        self.ui.leTaboo3.setText(taboo['tabues'][2])
        self.ui.leTaboo4.setText(taboo['tabues'][3])
        self.ui.leTaboo5.setText(taboo['tabues'][4])

    @QtCore.pyqtSlot()
    def on_pbGuardar_clicked(self):
        newTaboo = {}
        newTaboo['tabues'] = []
        newTaboo['palabra'] = unicode(self.ui.lePalabra.text().toUtf8(), 'utf-8')
        newTaboo['tabues'].append(unicode(self.ui.leTaboo1.text().toUtf8(), 'utf-8'))
        newTaboo['tabues'].append(unicode(self.ui.leTaboo2.text().toUtf8(), 'utf-8'))
        newTaboo['tabues'].append(unicode(self.ui.leTaboo3.text().toUtf8(), 'utf-8'))
        newTaboo['tabues'].append(unicode(self.ui.leTaboo4.text().toUtf8(), 'utf-8'))
        newTaboo['tabues'].append(unicode(self.ui.leTaboo5.text().toUtf8(), 'utf-8'))
        self.emit(QtCore.SIGNAL("tabooSaved"), self.editedTaboo, newTaboo)
        self.hide()

    def on_pbCancelar_clicked(self):
        self.hide()



if __name__ == '__main__':
	pass

