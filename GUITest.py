#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GUITest.py
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
import pyqtgraph.console
import numpy as np
from pyqtgraph.dockarea import *
import piplates.DAQC2plate as DAQC2
from Probe import *
from Control import *

#Create window/widget/dock
app = QtGui.QApplication([])
win = QtGui.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1000,500)
win.setWindowTitle('Logic Analyzer GUI Test')

probe1 = Dock("Probe1", size=(1, 1)) 
probe2 = Dock("Probe2", size=(1, 1)) 
probe3 = Dock("Probe3", size=(1, 1)) 
probe4 = Dock("Probe4", size=(1, 1)) 
Infodoc = Dock("Control Panel", size=(1, 1)) 

#Add docks to area
area.addDock(Infodoc, 'left')
area.addDock(probe1, 'bottom', Infodoc)
area.addDock(probe2, 'bottom', probe1)
area.addDock(probe3, 'bottom', probe2)
area.addDock(probe4, 'bottom', probe3)

def LogicAnalyzer():
	controler = Control()
	Infodoc.addWidget(controler)
	global probes
	probes = controler.getProbes()
	
	#Add plot Widgets to Docks	
	probe1.addWidget(probes[0])
	probe2.addWidget(probes[1])
	probe3.addWidget(probes[2])
	probe4.addWidget(probes[3])

def main(args):
	LogicAnalyzer()
	
	win.show()
	
	app.exec_()
	print("Close")
	global probes
	i=0
	for p in probes:
		print("\nP"+str(i)+": \n",p.getData())
		i+=1

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
