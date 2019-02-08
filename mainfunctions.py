# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# -------------------------------------GLP2-e Admin-------------------------------------
# -------------------------------------Version 2.0--------------------------------------
# ----------------------------Credits: David González Velasco---------------------------
# --------------------------Copyright: Boos Technical Lighting--------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# ------------------------------------Functions file------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

import sys
from tkinter import *
from tkinter import ttk 
import tkinter as tk
import tkinter.messagebox as mb
from winreg import *
from PIL import Image, ImageTk
import numpy as np
from ttkthemes import ThemedStyle
import ast
import threading
import time
import requests
import json
import threading
from collections import namedtuple

global testrunning
testrunning = False


class Preferences(object):
    def __init__(self,jsondata):
        self.usernumber = jsondata['usernumber']
        self.username = jsondata['username']
        self.usersurname = jsondata['usersurname']
        self.useremail = jsondata['useremail']
        self.userpassword = jsondata['userpassword']
        self.testmachineserialport = jsondata['testmachineserialport']
        self.testmachineserialbauds = jsondata['testmachineserialbauds']
        self.testmachineserialparity = jsondata['testmachineserialparity']
        self.testmachineserialbytesize = jsondata['testmachineserialbytesize']
        self.luxometerserialport = jsondata['luxometerserialport']
        self.luxometerserialbauds = jsondata['luxometerserialbauds']
        self.luxometerserialparity = jsondata['luxometerserialparity']
        self.luxometerserialbytesize = jsondata['luxometerserialbytesize']
        self.relaycardserialport = jsondata['relaycardserialport']
        self.relaycardserialbauds = jsondata['relaycardserialbauds']
        self.relaycardserialparity = jsondata['relaycardserialparity']
        self.relaycardserialbytesize = jsondata['relaycardserialbytesize']
        self.serverip = jsondata['serverip']
        self.languageselected = jsondata['languageselected']
        self.cameraenabled = jsondata['cameraenabled']
        self.onscreenresult = jsondata['onscreenresult']
        self.savecameraresults = jsondata['savecameraresults']
        self.luminaryprinter = jsondata['luminaryprinter']
        self.luminaryenabled = jsondata['luminaryenabled']
        self.luminaryprintingmode = jsondata['luminaryprintingmode']
        self.packagingprinter = jsondata['packagingprinter']
        self.packagingenabled = jsondata['packagingenabled']
        self.userguideprinter = jsondata['userguideprinter']
        self.userguideenabled = jsondata['userguideenabled']

    def dumpjson(self):
        jsondata = '{\n"usernumber":"'+self.usernumber+'",\n"username":"'+self.username+'",\n"usersurname":"'+self.usersurname+'",\n"useremail":"'+self.useremail+'",\n"userpassword":"'+self.userpassword+'",\n"testmachineserialport":"'+self.testmachineserialport+'",\n"testmachineserialbauds":"'+self.testmachineserialbauds+'",\n"testmachineserialparity":"'+self.testmachineserialparity+'",\n"testmachineserialbytesize":"'+self.testmachineserialbytesize+'",\n"luxometerserialport":"'+self.luxometerserialport+'",\n"luxometerserialbauds":"'+self.luxometerserialbauds+'",\n"luxometerserialparity":"'+self.luxometerserialparity+'",\n"luxometerserialbytesize":"'+self.luxometerserialbytesize+'",\n"relaycardserialport":"'+self.relaycardserialport+'",\n"relaycardserialbauds":"'+self.relaycardserialbauds+'",\n"relaycardserialparity":"'+self.relaycardserialparity+'",\n"relaycardserialbytesize":"'+self.relaycardserialbytesize+'",\n"serverip":"'+self.serverip+'",\n"languageselected":"'+self.languageselected+'",\n"cameraenabled":"'+self.cameraenabled+'",\n"onscreenresult":"'+self.onscreenresult+'",\n"savecameraresults":"'+self.savecameraresults+'",\n"luminaryprinter":"'+self.luminaryprinter+'",\n"luminaryenabled":"'+self.luminaryenabled+'",\n"luminaryprintingmode":"'+self.luminaryprintingmode+'",\n"packagingprinter":"'+self.packagingprinter+'",\n"packagingenabled":"'+self.packagingenabled+'",\n"userguideprinter":"'+self.userguideprinter+'",\n"userguideenabled":"'+self.userguideenabled+'"\n}'
        return(jsondata)

#Test machine functions
def calculateChecksum(command):
    data = bytes(command,'utf-8')
    checksum = 0 #Checksum started at 0
    checksum = checksum ^ 2  #Add STX value to the checksum
    checksum = checksum ^ 129 # Add ADR value to the checksum
    checksum = checksum ^ 250 # Add EMP value to the checksum

    for x in (data):
        checksum = checksum ^ x
    hexchecksum = hex(checksum)[2:4]
    if len(hexchecksum) < 2:
        hexchecksum = '0' + hexchecksum
    return(hexchecksum)

def sendSingleCommand(data):
    ser.port = myprefs.testmachineserialport
    try:
        ser.open()
    except Exception as e:
        flag=1
    if ser.isOpen():
        try:
            ser.flushInput()
            ser.flushOutput()
            ser.write(bytes(data,'iso-8859-1'))
            time.sleep(0.5)
            numberOfLines = 0
            while True:
                response = bytes.decode(ser.readline())
                response = ord(str(response))
                if response == ord(ACK):
                    responsereturned = True
                else:
                    responsereturned = False
                numberOfLines = numberOfLines + 1
                if (numberOfLines >=1):
                    break
            ser.close()
        except Exception as e1:
            print('Error communication...: ' + str(e1))
    else:
        pass
    return(responsereturned)

def sendDateTime():
    date = str(time.strftime('%w%y%d%m%H%M%S'))
    date = 'Z' + (date[::-1])
    datatosend = STX + ADR + EMP + date + checksum(date) + ETX
    response = sendSingleCommand(datatosend)
    return(response)

def sendProgram(program):
    programstring = '&load_' + program
    data = STX + ADR + EMP + programstring + checksum(programstring) + ETX
    response = sendSingleCommand(data)
    return(response)

def sendAndStartProgram(program):
    programstring = 's &load_' + program
    data = STX + ADR + EMP + programstring + checksum(programstring) + ETX
    respuesta = sendSingleCommand(data)
    return(response)

def receiveDataFromMachine():
    ser.port = myprefs.testmachineserialport
    try:
        ser.open()
    except Exception as e:
        pass
    if ser.isOpen:
        try:
            ser.flushInput()
            ser.flushOutput()
            ser.write(bytes(STX+ADR+ACK,'iso-8859-1'))
            time.sleep(0.5)
            numberOfLines = 0
            while True:
                response = ser.readline()
                numberOfLines = numberOfLines + 1
                if (numberOfLines >= 1):
                    break
        except Exception as e1:
            pass
    else:
        pass
    ser.close()
    return(response)


#Printers functions

def zebraReplaceChars(data):
    #This function replace the caracters of the textstring that is the Zebra Label to make it understandable to the printer
    data = data.replace('Á','_C3_81')
    data = data.replace('É','_C3_89')
    data = data.replace('Í','_C3_8D')
    data = data.replace('Ó','_C3_93')
    data = data.replace('Ú','_C3_9A')
    data = data.replace('Ñ','_C3_91')
    data = data.replace('á','_C3_A1')
    data = data.replace('é','_C3_A9')
    data = data.replace('í','_C3_AD')
    data = data.replace('ó','_C3_B3')
    data = data.replace('ú','_C3_BA')
    data = data.replace('ñ','_C3_B1')
    data = data.replace('º','_C2_B0')
    return(data)

def zebraPrintLabel(labelinfo):
    actualdir = os.getcwd()
    labelsdir
    if labelinfo.state == True:
        pass
    else:
        pass


def validateData(self,order):
    r = requests.post('http://127.0.0.1/webserviceproof/orderluminary.php',data={"a" : order.upper()})
    r =(r.text[3:-1])
    jsonfile = json.loads(r)

    ordertext = '#: '+jsonfile['order']+'\nState: '+jsonfile['state']+'\nQuantity: '+jsonfile['quantity']+'\nTest to realize: 1'
    self.element4.config(state=NORMAL)
    self.element4.delete(1.0, END)
    self.element4.insert(1.0,ordertext)
    self.element4.config(state=DISABLED)

    luminarytext = 'Code: '+jsonfile['lumcode']+'\nProgram: '+jsonfile['program']+'\nLed number: '+jsonfile['lednumber']+'\nOptic: '+jsonfile['optic']+'\nClass: '+jsonfile['electricalclass']+'\nPower consumption: '+jsonfile['syspower']+''
    self.element6.config(state=NORMAL)
    self.element6.delete(1.0, END)
    self.element6.insert(1.0,luminarytext)
    self.element6.config(state=DISABLED)

    luminarytext2= 'Dimming: '+jsonfile['dimming']+'\nDimming level: '+jsonfile['dimlevel']+'\nPhotocell: '+jsonfile['photocell']+'\nCLO: '+jsonfile['clo']+'\nLed Flux: '+jsonfile['flux']+'\nLed Color: '+jsonfile['ledcolor']+''
    self.element7.config(state=NORMAL)
    self.element7.delete(1.0, END)
    self.element7.insert(1.0,luminarytext2)
    self.element7.config(state=DISABLED)
    return(jsonfile)

def startTest(self,luminary):
    global testrunning
    def runTestMode():
        global testrunning
        #Start test mode

        def testGround():
            global testrunning
            #Ground Test
            while sendProgram('GROUND') == False:
                if testrunning == True:
                    time.sleep(0.60)
                else:
                    return('Cancelled')
            response = '-'
            while len(response) == 1:
                if testrunning == True:
                    time.sleep(0.60)
                    response = receiveDataFromMachine()
                else:
                    return('Cancelled')
            else:
                #Format the response and set values.
                response = str(response[4:-4]).replace(' ','|')[2:-1].split('|')
                groundmain = response[2]
                groundvalue = response[3]
                groundresult = response[4]

                if groundresult == 'IO':
                    #Update previous reserve
                    #
                    return('Continue')
                else:
                    #Update previous reserve
                    return('Failed')

        def testIsolate():
            global testrunning
            #Ground Test
            while sendProgram('ISOLATE') == 'N':
                if testrunning == True:
                    time.sleep(0.60)
                else:
                    return('Cancelled')
            response = '-'
            while len(response) == 1:
                if testrunning == True:
                    time.sleep(0.60)
                    response = receiveDataFromMachine()
                else:
                    return('Cancelled')
            else:
                #Format the response and set values.
                response = str(response[4:-4]).replace(' ','|')[2:-1].split('|')
                isolatemain = response[2]
                isolatevalue = response[3]
                isolateresult = response[4]

                if groundresult == 'IO':
                    #Update previous reserve
                    #
                    return('Continue')
                else:
                    #Update previous reserve
                    return('Failed')

        def testFunction():
            global testrunning
            #Ground Test
            while sendProgram('FUN') == 'N':
                if testrunning == True:
                    time.sleep(0.60)
                else:
                    return('Cancelled')
            response = '-'
            while len(response) == 1:
                if testrunning == True:
                    time.sleep(0.60)
                    response = receiveDataFromMachine()
                else:
                    return('Cancelled')
            else:
                #Format the response and set values.
                response = str(response[4:-4]).replace(' ','|')[2:-1].split('|')
                functionmain = response[2]
                functionvalue = response[3]
                functionresult = response[4]

                if groundresult == 'IO':
                    #Update previous reserve
                    #
                    return('Continue')
                else:
                    #Update previous reserve
                    return('Failed')

        def programPhilipsDALI():
            pass

        def programPhilipsSimpleset():
            pass

        def programVIAPAQ():
            pass

        def programLayrton():
            pass



    if testrunning == False:
        t.threading.Thread(target=runtestmode)
        t.start()
    else:
        print('The test is already running.')