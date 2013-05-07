#!/usr/bin/python
# -*- coding:Utf-8 -*-

# Copyright (C) 2008 Pâris Quentin
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import socket, threading, thread, os, time, random, string

from patterns.Observable import Observable
from models.Timer import Timer

class Directory(Observable):        
   def __init__(self, path):
       Observable.__init__(self)
       self.path = path
       self.content = None
       self.folderTime = 0
       self.refresh()
       
   # Timer
   def checkForChange(self, tempo = 1.0):
       self._timer = Timer(1.0, self.refresh)
       self._timer.start()
      
   def getFolderTime(self):
       try:
           return os.path.getmtime(self.path)
       except OSError: # Folder does not exist
           return 0
   
   def __iter__(self):
       return self.content.__iter__() 

   # Update shortcuts from folder, return True if changes have been made
   def refresh(self):
        folderTime = self.getFolderTime()
        if(folderTime != self.folderTime or self.content == None and self.folderTime != 0):
            self.folderTime = folderTime
            self.content = os.listdir(self.path)
            self.content.sort()
            # FIXME
            try :
                self.content.remove(".DS_Store")
            except ValueError:
                pass
                
            changed = True
            self.update()   
        else:
            changed = False
        
        return changed   
        
   def getList(self):
       return self.content
       
   def destroy(self):
       try:
           self._timer.stop()
       except AttributeError:
           pass