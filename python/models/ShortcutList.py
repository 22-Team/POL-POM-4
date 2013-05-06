#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2007-2013 PlayOnLinux Team

# python imports
import string, os, wx

from models.Observable import *
from models.Observer import *
from models.Shortcut import Shortcut

from models.Directory import Directory

from services.Environment import Environment
from services.ConfigService import ConfigService

class ShortcutList(Observer, Observable):
   def __init__(self, shortcutList = []):
       Observable.__init__(self)
       Observer.__init__(self)
       self.shortcutList = shortcutList[:]
       
   def getList(self):
       return self.shortcutList
       
class ShortcutListFromFolder(ShortcutList):  
   def __init__(self):
       ShortcutList.__init__(self)
       self.env = Environment()
       self._shortcutFolder = Directory(self.env.getUserRoot()+"/shortcuts/")
       self._iconsFolder = Directory(self.env.getUserRoot()+"/icones/full_size/")
       
       self._shortcutFolder.checkForChange()
       self._iconsFolder.checkForChange()
       
       self._shortcutFolder.register(self)
       self._iconsFolder.register(self)
              
   def notify(self):
       shortcutList = []   
       for ndx, member in enumerate(self._shortcutFolder):
           shortcutList.append(Shortcut(member))
       self.shortcutList = shortcutList
       self.update()
       
   def destroy(self):
       self._shortcutFolder.destroy()
       self._iconsFolder.destroy()