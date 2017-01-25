# -*- coding: utf-8 -*-
import os

# Qt imports
from PyQt4 import QtGui, uic, QtCore
import resources 
from PyQt4.QtCore import QSettings, pyqtSignal, pyqtSlot, SIGNAL, QObject
import qgis.utils
from gabarito import Gabarito
from PyQt4.QtGui import QSplitter, QPushButton, QComboBox, QIcon, QMessageBox
from PyQt4.Qt import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'gabarito.ui'))

class MainGabarito(QWidget,FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(MainGabarito, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.valores={}
        self.escala = None
        self.gabarito = None
        self.tamanho = None
        self.criarDict()
    
    def initGui(self):
        self.iface.digitizeToolBar().addWidget(self.escalasComboBox)
        self.iface.digitizeToolBar().addWidget(self.gabaritosComboBox)
        self.iface.digitizeToolBar().addWidget(self.tamanhosComboBox)
        self.iface.digitizeToolBar().addWidget(self.action1)
        
    def criarDict(self):
        self.tamanhos = {}
        self.tamanhos[u"25mm²"] = {'valor': 25, 'tipo': 'area'}
        self.tamanhos[u"4mm²"] = {'valor': 4, 'tipo': 'area'}
        self.tamanhos[u"1x1mm²"] = {'valor': 1, 'tipo': 'area'}
        self.tamanhos[u"0.8x0.8mm²"] = {'valor': 0.64, 'tipo': 'area'}
        self.tamanhos[u"0.8mm"] = {'valor': 0.8, 'tipo': 'distancia'}
    
    @pyqtSlot(int)
    def on_escalasComboBox_currentIndexChanged(self):
        if self.escalasComboBox.currentIndex() <> 0:
            self.escala = self.escalasComboBox.currentText()
    
    @pyqtSlot(int)
    def on_tamanhosComboBox_currentIndexChanged(self):
        if self.tamanhosComboBox.currentIndex() <> 0:
            self.tamanho = self.tamanhosComboBox.currentText()
            if self.tamanhosComboBox.currentText() == '0.8mm':
                self.gabaritosComboBox.setCurrentIndex(2)
                self.gabaritosComboBox.setEnabled(False)
            else:
                self.gabaritosComboBox.setEnabled(True)
    
    @pyqtSlot(int)
    def on_gabaritosComboBox_currentIndexChanged(self):
        if self.gabaritosComboBox.currentIndex() <> 0:
            self.gabarito = self.gabaritosComboBox.currentText()
            if self.tamanhosComboBox.currentText() == '0.8mm':
                self.gabaritosComboBox.setCurrentIndex(2)
                self.gabaritosComboBox.setEnabled(False)
            else:
                self.gabaritosComboBox.setEnabled(True)
    
    @pyqtSlot(bool)
    def on_action1_clicked(self):
        if self.escala and self.tamanho and self.gabarito:
            self.run()
        else:
            QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Valores do gabarito não definido :</font><br><font color=blue>Defina todos os valores para ativar o gabarito!</font>", QMessageBox.Close)    
    
    def unload(self):
        try:
            self.iface.mapCanvas().unsetMapTool(self.tool)

        except:
            pass           
    
    def run(self):
        if (self.tamanhos[self.tamanho]['tipo'] == 'area'):
            param = (float(self.escala)**2)*float(self.tamanhos[self.tamanho]['valor'])
        else:
            param = float(self.escala)*float(self.tamanhos[self.tamanho]['valor'])
        self.tool = Gabarito(self.iface.mapCanvas(), self.gabarito, param, self.tamanhos[self.tamanho]['tipo'] )
        self.tool.toolFinished.connect(self.refreshCombo)
        self.tool.setCursor(self.tool)		
        self.iface.mapCanvas().setMapTool(self.tool)			

    def refreshCombo(self):
        self.gabaritosComboBox.setEnabled(True)
