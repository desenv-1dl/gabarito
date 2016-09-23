# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import psycopg2, sys, os, csv, resources, qgis.utils 
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import qgis.utils
from gabarito import *



class MainGabarito:  

 
  def __init__(self, iface):

    self.iface = iface
    self.canvas = self.iface.mapCanvas()
    
    self.valores={}
  def initGui(self):
    

    mc = self.canvas
    layer = mc.currentLayer()
    self.grupo = QSplitter()

    self.action1 = QPushButton(QIcon(":/plugins/gabarito/icon.png"), u"gabarito", self.iface.mainWindow())

    
    
    self.criarCombo([u"ESCALAS",u"25",u"100",u"50"], u"ESCALAS")


    self.tamanhos = {}
    self.tamanhos[u"25mm²"] = {'valor': 25, 'tipo': 'area'}
    self.tamanhos[u"4mm²"] = {'valor': 4, 'tipo': 'area'}
    self.tamanhos[u"1x1mm²"] = {'valor': 1, 'tipo': 'area'}
    self.tamanhos[u"0.8x0.8mm²"] = {'valor': 0.64, 'tipo': 'area'}
    self.tamanhos[u"0.8mm"] = {'valor': 0.8, 'tipo': 'distancia'}
    valores=[u"TAMANHOS"]+self.tamanhos.keys()
    
    self.criarCombo(valores, u"TAMANHOS")

    self.criarCombo([u"GABARITOS",u"Hexágono",u"Quadrado"], u"GABARITOS")

    self.grupo.addWidget(self.action1)	
    
    
    
    QObject.connect(self.action1, SIGNAL("clicked()"), self.run)

    #self.iface.digitizeToolBar().addWidget(self.grupo)   
    self.iface.addToolBarWidget(self.grupo)

  def criarCombo(self, mapValores, nome):

	actionCB=QComboBox()
	actionCB.setObjectName(nome)
	for x in mapValores:
		actionCB.addItem(x, x)
	if nome == u"GABARITOS":
		self.gabarito=actionCB
        self.grupo.addWidget(actionCB)		
	self.valorCombo(actionCB)
	
  def valorCombo(self, combo=None):	
	def valorC(item):
		self.valores[unicode(combo.objectName())]=unicode(item)	
	self.valores[unicode(combo.objectName())]=""
	valorC(unicode(combo.currentText()))
	QObject.connect(combo, SIGNAL("activated(const QString&)"), valorC)    
 
  def unload(self):
	try:
    		self.iface.mapCanvas().unsetMapTool(self.tool)
	except:
		pass
    
            
   
  def run(self):
	print self.valores
	if (not self.valores.get(u"GABARITOS") == u"GABARITOS") and (not self.valores.get(u"ESCALAS") == u"ESCALAS") and (not self.valores.get(u"TAMANHOS") == u"TAMANHOS"):

		if self.tamanhos[self.valores.get(u"TAMANHOS")]['tipo'] == 'area':
			area = (float(self.valores.get(u"ESCALAS"))**2)*float(self.tamanhos[self.valores.get(u"TAMANHOS")]['valor'])
			self.tool = Gabarito(self.iface.mapCanvas(), self.valores.get(u"GABARITOS"), area, 'area' )

		else:
			self.valores[u"GABARITOS"]=u"Hexágono"
			index=self.gabarito.findData(u"Hexágono")
			self.gabarito.setCurrentIndex(index)

			tamanho = float(self.valores.get(u"ESCALAS"))*float(self.tamanhos[self.valores.get(u"TAMANHOS")]['valor'])
			self.tool = Gabarito(self.iface.mapCanvas(), u"Hexágono", tamanho, 'distancia' )
		self.tool.setCursor(self.tool)		
		self.iface.mapCanvas().setMapTool(self.tool)			
	else:
		QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Valores do gabarito não definido :</font><br><font color=blue>Defina todos os valores para ativar o gabarito!</font>", QMessageBox.Close)	
	  


