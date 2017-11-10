#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Settings.py
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
from Probe import *
 
class Control(pg.LayoutWidget):
	supportedProtocols = ['I2C','SPI']
	probeDef = {'I2C': ['SDA', 'SCK','Disabled', 'Disabled'], 'SPI': ['MOIS','SCK','MISO','SS']}
	currentProtocol = 'SPI'
	
	def __init__(self):
		super(Control,self).__init__()
		self.createObjects()
		self.probes = self.createProbes()
		
	def createObjects(self):
		self.label = QtGui.QLabel("""-- Logic Analyzer --""")
		self.startBtn = QtGui.QPushButton('Start Recording')
		self.stopNanalyzeBtn = QtGui.QPushButton('Stop Recording and Analyize')
		self.stopNanalyzeBtn.setEnabled(False)
		self.clearBtn = QtGui.QPushButton('Clear All Plots')
		self.protocolSelector = QtGui.QComboBox()
		self.protocolSelector.addItems(self.supportedProtocols)
		self.protocolSelector.currentIndexChanged.connect(self.protocolSelected)
		
		self.startBtn.clicked.connect(self.startRecording)
		self.stopNanalyzeBtn.clicked.connect(self.stopRecording)
		self.clearBtn.clicked.connect(self.clearPlots)
		
		self.addWidget(self.label, row=0, col=0)
		self.addWidget(self.protocolSelector, row=1, col=1)
		self.addWidget(self.startBtn, row=3, col=1)
		self.addWidget(self.stopNanalyzeBtn, row=4, col=1)
		self.addWidget(self.clearBtn, row=5, col=1)

	def protocolSelected(self):
		currentProtocol = self.protocolSelector.currentText()
		if currentProtocol == 'SPI':
			i=0
			#All 4 probes will be visible
			#Change names per list 
			for probe in self.probes:
				probe.setTitle(self.probeDef['SPI'][i])
				if self.probeDef['SPI'][i] == 'Disabled':
					probe.setEnabled(False)
				else:
					probe.setEnabled(True)
				i+=1
			
		if currentProtocol == 'I2C':
			i=0
			for probe in self.probes:
				probe.setTitle(self.probeDef['I2C'][i])
				if self.probeDef['I2C'][i] == 'Disabled':
					probe.setEnabled(False)
				else:
					probe.setEnabled(True)
				i+=1
		
	def startRecording(self):
		#Enable stop button
		self.stopNanalyzeBtn.setEnabled(True)
		#Disable start button
		self.startBtn.setEnabled(False)
		for p in self.probes:
			p.startRecording()
		
	def stopRecording(self):
		#Disable stop
		self.stopNanalyzeBtn.setEnabled(False)
		#Enable start button
		self.startBtn.setEnabled(True)
		for p in self.probes:
			p.stopRecording()
			
	def clearPlots(self):
		for probe in self.probes:
			probe.clear()		
			
	def createProbes(self):
		probes = []
		p1 = Probe(name='Probe1', title='SDA', pin = 0, enabled=True)
		p2 = Probe(name='Probe2', title='SCK', pin = 1, enabled=True)
		p3 = Probe(name='Probe3', title='Disabled', pin = 2, enabled=False)
		p4 = Probe(name='Probe4', title='Disabled', pin = 3, enabled=False)
		
		probes.append(p1)
		probes.append(p2)
		probes.append(p3)
		probes.append(p4)
		
		#Link Plots
		p2.setXLink('Probe1')
		p3.setXLink('Probe1')
		p4.setXLink('Probe1')
		
		return probes
	
	def getProbes(self):
		return self.probes
		
