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

import socket, threading, thread, os, wx, time, random
import string

from lib.Context import Context
from lib.UIHelper import UIHelper

class Queue():        
    def __init__(self): 
      self.queue = []
      
    def __str__(self):
        return str(self.queue)
        
    def add(self, array):
      self.queue.append(array)

    def isEmpty(self):
      return (self.queue == [])
      
    def shift(self):
      self.queue = self.queue[1:]
      
    def getTask(self):
      return self.queue[0]