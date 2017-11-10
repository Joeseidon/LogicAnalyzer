#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  probeThread.py
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


from pyqtgraph.Qt import QtCore, QtGui
import piplates.DAQC2plate as DAQC2
import time

class ProbeThread(QtCore.QThread):
	def __init__(self,pin):
		super(ProbeThread,self).__init__()
		self.pin = pin
	newData = QtCore.Signal(object)
	def run(self):
		while True:
			data = DAQC2.getDINbit(0,self.pin)
			self.newData.emit(data)
			time.sleep(0.05)
