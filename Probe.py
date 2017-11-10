#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Probe.py
#  
#  Copyright 2017  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import piplates.DAQC2plate as DAQC2

class Probe(pg.PlotWidget):
	def __init__(self, name, title, pin,enabled=True):
		super(Probe,self).__init__(name=name, title=title, labels = {'left':'Logic Level','bottom':'Time'})
		self.name = name
		self.title = title
		self.createCurve()
		self.createTimer()
		self.record = False
		self.enabled = enabled
		self.pdata = [1]
		self.pin = pin				

	def createCurve(self, enableShadow=False, enableRec=False):
		self.pcurve = self.getPlotItem().plot()
		self.pcurve.setPen('g')  ## white pen
		self.setYRange(0,1)
		self.setMouseEnabled(x=True,y=False)
		if enableShadow:
			pcurve1.setShadowPen(pg.mkPen((70,70,30), width=6, cosmetic=True))
		if enableRec:
			lr1 = pg.LinearRegionItem([1, 30], bounds=[0,100], movable=True)
			pWdg1.addItem(lr1)
			line1 = pg.InfiniteLine(angle=90, movable=True)
			pWdg1.addItem(line1)
			line1.setBounds([0,200])
			
	def createTimer(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.probeUpdater)
		
	def probeUpdater(self):
		if self.record and self.enabled:			
			pinReading = DAQC2.getDINbit(0,self.pin)
			self.pdata.append(pinReading)
			self.pcurve.setData(self.pdata)
			
	def startRecording(self):
		self.timer.start(1)
		self.record = True 
	
	def stopRecording(self):
		self.timer.stop()
		self.record = False
		
	def recording(self):
		return self.record
	
	def setEnabled(self, enabled):
		self.enabled = enabled
	
	def getData(self):
		return self.pdata
