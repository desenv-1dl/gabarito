# -*- coding: utf-8 -*-
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from math import *
import main

class Gabarito(QgsMapTool):

    def __init__(self, canvas, GEOMETRIA, AREA, TIPO):
        self.canvas = canvas
        self.active = False
	self.GEOMETRIA=GEOMETRIA
	self.area=AREA
	self.TIPO=TIPO
	self.cursor=None
        QgsMapTool.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
	
	if self.TIPO == 'area':
        	mFillColor = QColor( 254, 178, 76, 63 );
	else:
        	mFillColor = QColor( 255, 255, 0, 63 );
		
        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)
        self.reset()
    
    
    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
	try:
        	self.rubberBand.reset(QGis.Polygon)
    	except:
		pass

    def setCursor(self, cursor):
	self.cursor=cursor

    def canvasPressEvent(self, e):
	if self.cursor != None:
    		self.canvas.unsetMapTool(self.cursor)

    def canvasMoveEvent(self, e):

        self.endPoint = self.toMapCoordinates( e.pos() )

	if self.GEOMETRIA == u"Hexágono":
		self.showHex(self.endPoint, self.area)
    	elif self.GEOMETRIA == u"Quadrado":
		self.showRect(self.endPoint, self.area)




    def showHex(self, startPoint, area):
	self.rubberBand.reset(QGis.Polygon)
        
	if self.TIPO == 'area':
		lado = sqrt(2*area*sqrt(3))/3

		point1 = QgsPoint(startPoint.x() - lado, startPoint.y())
		point2 = QgsPoint(startPoint.x() - lado/2, startPoint.y() + lado*sqrt(3)/2)
		point3 = QgsPoint(startPoint.x() + lado/2, startPoint.y() + lado*sqrt(3)/2)
		point4 = QgsPoint(startPoint.x() + lado, startPoint.y())
		point5 = QgsPoint(startPoint.x() + lado/2, startPoint.y() - lado*sqrt(3)/2)
		point6 = QgsPoint(startPoint.x() - lado/2, startPoint.y() - lado*sqrt(3)/2)

	else:
		lado = area
		point1 = QgsPoint(startPoint.x() - lado, startPoint.y())
		point2 = QgsPoint(startPoint.x() - lado/2, startPoint.y() + lado*sqrt(3)/2)
		point3 = QgsPoint(startPoint.x() + lado/2, startPoint.y() + lado*sqrt(3)/2)
		point4 = QgsPoint(startPoint.x() + lado, startPoint.y())
		point5 = QgsPoint(startPoint.x() + lado/2, startPoint.y() - lado*sqrt(3)/2)
		point6 = QgsPoint(startPoint.x() - lado/2, startPoint.y() - lado*sqrt(3)/2)



        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, False)
        self.rubberBand.addPoint(point5, False) 
        self.rubberBand.addPoint(point6, True)    # true to update canvas
        self.rubberBand.show()

    def showRect(self, startPoint, area):
	 
        self.rubberBand.reset(QGis.Polygon)
        point1 = QgsPoint(startPoint.x() - sqrt(area)/2, startPoint.y() - sqrt(area)/2)
        point2 = QgsPoint(startPoint.x() - sqrt(area)/2, startPoint.y() + sqrt(area)/2)
        point3 = QgsPoint(startPoint.x() + sqrt(area)/2, startPoint.y() + sqrt(area)/2)
        point4 = QgsPoint(startPoint.x() + sqrt(area)/2, startPoint.y() - sqrt(area)/2)

        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)
        self.rubberBand.show()


    
    def deactivate(self):
        self.rubberBand.hide()
        QgsMapTool.deactivate(self)
        
    def activate(self):
        QgsMapTool.activate(self)
        
