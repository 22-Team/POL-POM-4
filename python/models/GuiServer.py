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

import socket, threading, thread, os, wx, time, random, select
import string

from models.PlayOnLinux import PlayOnLinux
from models.Queue import Queue
from models.GuiServerState import GuiServerState


class ErrServerIsNotRunning(Exception):
   def __str__(self):
      return repr(_("The server is not running"))
      
class GuiServer(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self)
        self.daemon = True
        self.host = '127.0.0.1'
        self.runningPort = 0
        self.tryingPort = 30000
    
        self._running = True
        self.cookie = None
        
        self.queue = Queue()
        self.state = GuiServerState()
            
    def getQueue(self):
        return self.queue
        
    def getState(self):
        return self.state
            
    def getRunningPort(self):
        return self.runningPort
        
    def setRunningPort(self, port):
        self.runningPort = port  
        
    def successRunServer(self):
        self.runningPort = self.tryingPort

    def getCookie(self, length=20, chars=string.letters + string.digits):
        if(self.cookie == None):
            self.cookie = ''.join([random.SystemRandom().choice(chars) for i in range(length)])
        return self.cookie
        

    def isServerRunning(self):
        return self.runningPort != 0
        
    def waitForServer(self):
        i = 0
        
        while(not self.isServerRunning()):
            time.sleep(0.01)
            if(i >= 300):
                # Fixme! 
                Error('[APP] is not able to start [APP] Setup Window server.')
                os._exit(0)
                break
            i+=1
            
           
    def initServer(self):
        if(self.tryingPort  >= 30020):
           print _("Error: Unable to reserve a valid port")
           wx.MessageBox(_("Error: Unable to reserve a valid port"),PlayOnLinux().getAppName())
           os._exit(0)
           
        try:
           self.acceptor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           self.acceptor.bind ( ( str(self.host), int(self.tryingPort) ) )
           self.acceptor.listen(10)
           self.successRunServer()
           
        except socket.error, msg:       
           self.tryingPort += 1;
           self.initServer()
        

    def closeServer(self):
        try:
            self.acceptor.close()
        except AttributeError:
            raise ErrServerIsNotRunning
            
        self._running = False

    def processReceivedData(self, recvData):
       recvData = recvData.split("\t")
       pid = recvData[2]
       if(recvData[0] != self.getCookie()):
           print "Bad cookie!"
           return ""

       recvData = recvData[1:]
       self.queue.add(recvData)
       self.state.set(pid, None)
       
       # Wait until GUI has send a new answer
       while True:

           dataFromGui = self.state.read(pid)
           
           if(dataFromGui != None):
               return dataFromGui
            
           time.sleep(0.1)   


    
    def handler(self, connection, addr):
        data = "";
        while True:
            buff = connection.recv(2048);
           
            data += buff
            if "\n" in buff:
                data = data.replace("\n","")
                break;

        connection.send(self.processReceivedData(data))
        
        connection.shutdown(1)
        connection.close()
               
    def run(self): 
        self.initServer()
        while self._running:        
            connection, addr = self.acceptor.accept()
            thread.start_new_thread(self.handler, (connection, addr))

        