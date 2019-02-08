#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#-------------------------------------GLP2-e Admin-------------------------------------
#-------------------------------------Version 2.0--------------------------------------
#----------------------------Credits: David González Velasco---------------------------
#--------------------------Copyright: Boos Technical Lighting--------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#------------------------Library for the Graphic User Interface------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

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
import mainfunctions as fn


def getAccentColor():
    """
    Return the Windows 10 accent color used by the user in a HEX format
    """
    #Open the registry
    registry = ConnectRegistry(None,HKEY_CURRENT_USER)
    #Navigate to the key that contains the accent color info
    key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Accent')
    # Read the value in a REG_DWORD format
    key_value = QueryValueEx(key,'AccentColorMenu')
    #Convert the interger to Hex and remove its offset
    accent_int = key_value[0]
    accent_hex = hex(accent_int+4278190080) #Remove FF offset and convert to HEX again
    accent_hex = str(accent_hex)[5:] #Remove prefix and suffix
    #The HEX value was originally in a BGR order, instead of RGB,
    #so we reverse it...
    accent = accent_hex[4:6]+accent_hex[2:4]+accent_hex[0:2] #BGR
    return('#'+accent)

def getDarkModeState():
    #Return the Windows 10 variable that indicates if the dark mode is enabled or not
    #Open the registry
    registry = ConnectRegistry(None,HKEY_CURRENT_USER)
    #Navigate to the key that contains the accen t color info
    key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
    #Read the value in a REG_DWORD format
    key_value = QueryValueEx(key,'AppsUseLightTheme')
    #Convert the interger to Hex and remove its offset
    darkmodestate = key_value[0]
    return(darkmodestate)

def dynamicBackground():
    if getDarkModeState() == 0:
        return('#000000')
    else:
        return('#ffffff')

def dynamicForeground():
    if getDarkModeState() == 0:
        return('#ffffff')
    else:
        return('#000000')

def changeImageColorToAccentColor(imagename):
    imagename = str(imagename)
    print(str(imagename).split('/')[len(str(imagename).split('/'))-1])
    accent = str(getAccentColor().lstrip('#'))


    rcolor = int(str(accent[0:2]),16)
    gcolor = int(str(accent[2:4]),16)
    bcolor = int(str(accent[4:6]),16)

    im = Image.open(str(imagename))
    im = im.convert('RGBA')

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
    data[..., :-1][white_areas.T] = (rcolor, gcolor, bcolor) # Transpose back needed

    im2 = Image.fromarray(data)
    im2.save('colorchanged.png')

    size = 128, 128

    im2.thumbnail(size)
    im2.show()
    im2.save('colorchanged128x128.png')

def makeIcon(file, height=50, width=50, mode='color',color=''):
    #This function works equally as the ImageTk.PhotoImage but with some added capabilities.

    #Works like:
    #im = makeIcon('ROUTETOFILE.PNG',height=100,width=100,mode='white')
    #icon = Label(frame1,image=im)

    imagename = str(file)
    accent = str(getAccentColor().lstrip('#'))

    rcolor = int(str(accent[0:2]),16)
    gcolor = int(str(accent[2:4]),16)
    bcolor = int(str(accent[4:6]),16)

    im = Image.open(str(imagename))
    im = im.convert('RGBA')

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    if mode == 'color':
        white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
        data[..., :-1][white_areas.T] = (rcolor, gcolor, bcolor) # Transpose back needed
    elif mode == 'dynamic':
        if getDarkModeState() == 1:
            white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
            data[..., :-1][white_areas.T] = (0, 0, 0) # Transpose back needed
        else:
            white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
            data[..., :-1][white_areas.T] = (255, 255, 255)  # Transpose back needed
    elif mode == 'manual':
        color = color.lstrip('#')
        rcolor = int(str(color[0:2]),16)
        gcolor = int(str(color[2:4]),16)
        bcolor = int(str(color[4:6]),16)
        white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
        data[..., :-1][white_areas.T] = (rcolor, gcolor, bcolor)
    else:
        raise TypeError("Mode can only be 'color' or 'dynamic'.")

    im2 = Image.fromarray(data)
    size = (height, width)
    im2.thumbnail(size)

    image1 = ImageTk.PhotoImage(im2)
    return(image1)

def switchColor(file,height=50, width=50, mode='color'):
    #This function works equally as the ImageTk.PhotoImage but with some added capabilities.

    #Works like:
    #im = makeIcon('ROUTETOFILE.PNG',height=100,width=100,mode='white')
    #icon = Label(frame1,image=im)

    imagename = str(file)
    accent = str(getAccentColor().lstrip('#'))

    rcolor = int(str(accent[0:2]),16)
    gcolor = int(str(accent[2:4]),16)
    bcolor = int(str(accent[4:6]),16)

    im = Image.open(str(imagename))
    im = im.convert('RGBA')

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    if mode == 'color':
        white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
        data[..., :-1][white_areas.T] = (rcolor, gcolor, bcolor) # Transpose back needed


    elif mode == 'dynamic':
        if getDarkModeState() == 1:
            white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
            data[..., :-1][white_areas.T] = (0, 0, 0) # Transpose back needed
        else:
            white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
            data[..., :-1][white_areas.T] = (255, 255, 255)  # Transpose back needed
    elif mode == 'none':
        pass
    else:
        raise TypeError("Mode can only be 'color' or 'dynamic'.")

    im2 = Image.fromarray(data)
    size = (height, width)
    im2.thumbnail(size)

    image1 = ImageTk.PhotoImage(im2)
    return(image1)

def radioColor(file,height=50, width=50, mode='color'):
    #This function works equally as the ImageTk.PhotoImage but with some added capabilities.

    #Works like:
    #im = makeIcon('ROUTETOFILE.PNG',height=100,width=100,mode='white')
    #icon = Label(frame1,image=im)

    imagename = str(file)
    accent = str(getAccentColor().lstrip('#'))

    rcolor = int(str(accent[0:2]),16)
    gcolor = int(str(accent[2:4]),16)
    bcolor = int(str(accent[4:6]),16)

    im = Image.open(str(imagename))
    im = im.convert('RGBA')

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    if mode == 'color':
        white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
        data[..., :-1][white_areas.T] = (rcolor, gcolor, bcolor) # Transpose back needed


    elif mode == 'dynamic':
        if getDarkModeState() == 1:
            white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
            data[..., :-1][white_areas.T] = (0, 0, 0) # Transpose back needed
        else:
            white_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
            data[..., :-1][white_areas.T] = (255, 255, 255)  # Transpose back needed
    elif mode == 'none':
        pass
    else:
        raise TypeError("Mode can only be 'color' or 'dynamic'.")

    im2 = Image.fromarray(data)
    size = (height, width)
    im2.thumbnail(size)

    image1 = ImageTk.PhotoImage(im2)
    return(image1)

def dynamicSizeImage():
    pass

mainfont = "-family {Segoe UI} -size 11 -weight normal "  \
                "-slant roman -underline 0 -overstrike 0"

mainfontbold = "-family {Segoe UI} -size 11 -weight bold "  \
                "-slant roman -underline 0 -overstrike 0"

subfont = "-family {Segoe UI} -size 10 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

subdescfont = "-family {Segoe UI Light} -size 9 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlefont = "-family {Segoe UI Semilight} -size 18 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlefontbig = "-family {Segoe UI Semilight} -size 25 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlelightfont = "-family {Segoe UI Light} -size 18 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlebold = "-family {Segoe UI} -size 20 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlefont15 = "-family {Segoe UI Semilight} -size 15 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlefont15bold = "-family {Segoe UI} -size 15 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlelightfont15 = "-family {Segoe UI Light} -size 15 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

titlefont13bold = "-family {Segoe UI} -size 13 -weight bold -slant "  \
                "roman -underline 0 -overstrike 0"

class SidebarTopTitle(object):
    def __init__(self,parent='*',placeholder='',state='normal',icon='mainicons/settings32.png'):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')

        self.height=60
        self.width=parent.width
        self.placeholder = placeholder

        def titleenter(event):
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#343434')
                titlelabel.configure(background='#343434')
                titleicon.configure(background='#343434')
            else:
                self.widgetname.configure(background='#dadada')
                titlelabel.configure(background='#dadada')
                titleicon.configure(background='#dadada')
        def titleleave(event):
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#000000')
                titlelabel.configure(background='#000000')
                titleicon.configure(background='#000000')
            else:
                self.widgetname.configure(background='#ffffff')
                titlelabel.configure(background='#ffffff')
                titleicon.configure(background='#ffffff')
        def titleclicked(event):
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#898989')
                titlelabel.configure(background='#898989')
                titleicon.configure(background='#898989')
            else:
                self.widgetname.configure(background='#939393')
                titlelabel.configure(background='#939393')
                titleicon.configure(background='#939393')


        self.widgetname = Frame(self.parent,width=self.width,height=self.height)


        iconimage = PhotoImage(file=icon)

        if getDarkModeState() == 0:
            titleicon = Label(self.widgetname,image=iconimage,background='#000000')
            titlelabel = Label(self.widgetname,text=self.placeholder,font=titlefont,background='#000000')
            titlelabel.configure(foreground='#ffffff')
            self.widgetname.configure(background='#000000')
        else:
            titleicon = Label(self.widgetname,image=iconimage,background='#ffffff')
            titlelabel = Label(self.widgetname,text=self.placeholder,font=titlefont,background='#ffffff')
            titlelabel.configure(foreground='#000000')
            self.widgetname.configure(background='#ffffff')

        titleicon.image = iconimage

        self.widgetname.bind('<Enter>',titleenter)
        titlelabel.bind('<Enter>',titleenter)
        titleicon.bind('<Enter>',titleenter)

        self.widgetname.bind('<Leave>',titleleave)
        titlelabel.bind('<Leave>',titleleave)
        titleicon.bind('<Leave>',titleleave)

        self.widgetname.bind('<Button-1>',titleclicked)
        titlelabel.bind('<Button-1>',titleclicked)
        titleicon.bind('<Button-1>',titleclicked)

        self.widgetname.bind('<ButtonRelease-1>',titleenter)
        titlelabel.bind('<ButtonRelease-1>',titleenter)
        titleicon.bind('<ButtonRelease-1>',titleenter)

        titleicon.place(x=10,y=0,height=60)
        titlelabel.place(x=52,y=0,height=60)


    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0,width=320):
        self.x = x
        self.y = y
        self.width = width
        self.widgetname.place(x=self.x,y=self.y,height=self.height,width=self.width)

    def pack():
        pass

class SidebarSectionTitle(object):
    pass

class SidebarSectionElement(object):
    pass

class TextEntry(object):
    #Constructor de la clase
    def __init__(self,parent='*',text='*',placeholder='*',state='normal',show=None,action=False):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')

        self.height=32
        self.width=150
        self.placeholder = placeholder
        self.text = text
        self.state = state
        self.show = show
        self.action = action

        if self.text == '*' and self.placeholder == '*':
            raise TypeError("You can't define a TextEntry widget with text and placeholder.\nPlease, set only one of the two options.")
        else:
            if self.text != '*':
                self.type = 'textmode'
            elif self.placeholder != '*':
                self.type = 'placeholdermode'
            else:
                self.type ='undefinedmode'

        def defocuswidget(event):
            parent.focus()
        def entryfocusin(event):
            self.widgetname.configure(background=getAccentColor())
            if self.type == 'placeholdermode':
                if self.entry.get() == self.placeholder:
                    self.entry.configure(show=self.show)
                    self.entry.icursor(0)
                    self.entry.delete(0,'end')
                else:
                    pass
            else:
                pass
            self.entry.configure(foreground='#000000',background='#ffffff')
        def entryfocusout(event):
            self.widgetname.configure(background='#939393')
            if self.type == 'placeholdermode':
                if self.entry.get() == '':
                    self.entry.configure(show='')
                    self.entry.insert(0,str(self.placeholder))
                else:
                    pass
            if getDarkModeState() == 0:
                self.entry.configure(foreground='#939393',background='#000000')
            else:
                self.entry.configure(foreground='#939393',background='#ffffff')
            if self.action != False:
                self.action(self)
            else:
                pass
        def entryenter(event):
            parent.unbind_all('<Button-1>')
            if parent.focus_get() == self.entry:
                pass
            else:
                if getDarkModeState() == 0:
                    self.widgetname.configure(background='#efefef')
                    self.entry.configure(foreground='#efefef')
                else:
                    self.widgetname.configure(background='#696969')
                    self.entry.configure(foreground='#696969')
        def entryleave(event):
            parent.bind_all('<Button-1>',defocuswidget)
            if parent.focus_get() == self.entry:
                pass
            else:
                self.widgetname.configure(background='#939393')
                self.entry.configure(foreground='#939393')

        self.widgetname = Frame(self.parent)
        self.widgetname.configure(borderwidth='2',background='#939393')

        self.entry = Entry(self.widgetname,state=self.state)

        if self.show == None:
            pass
        else:
            self.entry.configure(show=self.show)
        if getDarkModeState() == 0:
            self.entry.configure(background='#000000',relief=FLAT,foreground='#939393',selectbackground=getAccentColor(),disabledbackground='#939393',disabledforeground='#000000',font=mainfont)
        else:
            self.entry.configure(background='#ffffff',relief=FLAT,foreground='#939393',selectbackground=getAccentColor(),disabledbackground='#939393',disabledforeground='#ffffff',font=mainfont)
        if self.type == 'textmode':
            self.entry.insert(0,str(self.text))
        elif self.type == 'placeholdermode':
            self.entry.insert(0,str(self.placeholder))
        elif self.type == 'undefinedmode':
            pass
        self.entry.bind('<FocusIn>',entryfocusin)
        self.entry.bind('<FocusOut>',entryfocusout)

        self.widgetname.bind('<Enter>',entryenter)
        self.entry.bind('<Enter>',entryenter)
        self.widgetname.bind('<Leave>',entryleave)
        self.entry.bind('<Leave>',entryleave)

    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0,width=150):
        self.x = x
        self.y = y
        self.width = width

        self.widgetname.pack()
        self.widgetname.place(x=self.x,y=self.y,height=self.height,width=self.width)
        self.entry.pack()
        self.entry.place(x=0,y=0,height=28,width=self.width-4)

    def pack():
        pass
    def insert(self,text=''):
        self.entry.icursor(0)
        self.entry.delete(0,'end')
        self.entry.insert(0,str(text))

    def get(self):
        text = self.entry.get()
        return(text)

    def insert(self,text='*'):
        if text != self.placeholder:
            self.entry.configure(show=self.show)
            self.entry.delete(0,'end')
            self.entry.insert(0,str(text))
            self.text = text
        else:
            pass

class CheckBox(object):
    def __init__(self,parent='*',placeholder='',state=False, action=None):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')
        self.placeholder = placeholder
        if state == True or state == False:
            self.state = state
        else:
            raise TypeError('The state of this widget must be a Boolean (True/False)')

        self.height=20
        self.action = action

        def defocuswidget(event):
            parent.focus()
        def checkselector(event):
            self.widgetname.focus()
            if self.state == False:
                self.check.configure(background=getAccentColor())
                self.check.place_forget()
                self.tick.pack()
                self.state = True
            else:
                self.check.configure(background=dynamicBackground(),relief=FLAT)
                self.check.place(x=0,y=0,height=16,width=16)
                self.tick.forget()
                self.state = False
            if self.action != None:
                self.action()
        def checkenter(event):
            self.widgetname.bind_all('<Return>',checkselector)
            self.widgetname.bind_all('<space>',checkselector)
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#ffffff')
            else:
                self.widgetname.configure(background='#000000')
        def checkleave(event):
            parent.bind_all('<Button-1>',defocuswidget)
            self.widgetname.unbind_all('<Return>')
            self.widgetname.unbind_all('<space>')
            if self.state == True:
                self.widgetname.configure(background=getAccentColor())
            else:
                self.widgetname.configure(background='#939393')


        self.widgetname = Frame(self.parent,takefocus=True)
        self.widgetname.configure(borderwidth='2',background='#939393')

        self.check = Frame(self.widgetname)
        if self.state == False:
            if getDarkModeState() == 0:
                self.check.configure(background='#000000',relief=FLAT)
            else:
                self.check.configure(background='#ffffff',relief=FLAT)
        else:
            self.check.configure(background=getAccentColor(),relief=FLAT)



        tickpng = PhotoImage(file='mainicons/interface/tick.png')
        self.tick = Label(self.widgetname,background=getAccentColor(),image=tickpng)
        self.tick.image = tickpng


        self.check.bind('<Button-1>',checkselector)
        self.tick.bind('<Button-1>',checkselector)
        self.check.bind('<Enter>',checkenter)
        self.tick.bind('<Enter>',checkenter)
        self.check.bind('<Leave>',checkleave)
        self.tick.bind('<Leave>',checkleave)
        self.widgetname.bind('<FocusIn>',checkenter)
        self.widgetname.bind('<FocusOut>',checkleave)

        if self.placeholder == '':
            pass
        else:
            self.checkplaceholder = Label(self.parent,text=self.placeholder,font=mainfont)
            self.checkplaceholder.bind('<Enter>',checkenter)
            self.checkplaceholder.bind('<Leave>',checkleave)
            self.checkplaceholder.bind('<Button-1>',checkselector)
            if getDarkModeState() == 0:
                self.checkplaceholder.configure(background='#000000',foreground='#ffffff')
            else:
                self.checkplaceholder.configure(background='#ffffff',foreground='#000000')

    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0):
        self.x = x
        self.y = y

        self.widgetname.pack()
        self.widgetname.place(x=self.x,y=self.y,height=self.height,width=20)
        self.check.place(x=0,y=0,height=16,width=16)
        self.checkplaceholder.pack()
        self.checkplaceholder.place(x=self.x+25,y=self.y-3)
    def get(self):
        text = self.state.get()
        return(text)

class Switch(object):
    def __init__(self,parent='*',placeholder='*',state=False,action=None):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')

        if placeholder != '*':
            self.placeholder = placeholder
        else:
            raise TypeError('You must select a placeholder for the widget.')
        if state == True or state == False:
            self.state = state
        else:
            raise TypeError('The state of this widget must be a Boolean (True/False)')

        self.height=20
        self.action = action

        def defocuswidget(event):
            parent.focus()
        def switchchangemode(event):
            self.widgetname.focus()
            if self.state == False:
                switchpng = switchColor(file='mainicons/interface/switchselectedon.png',height=40,width=40,mode='none')
                self.switch.configure(image=switchpng)
                self.switch.image = switchpng
                self.state = True
            else:
                switchpng = switchColor(file='mainicons/interface/switchselectedoff.png',height=40,width=40,mode='none')
                self.switch.configure(image=switchpng)
                self.switch.image = switchpng
                self.state = False
            if self.action != None:
                self.action()
        def checkenter(event):
            self.widgetname.bind_all('<Return>',switchchangemode)
            self.widgetname.bind_all('<space>',switchchangemode)
            if self.state == True:
                switchpng = switchColor(file='mainicons/interface/switchselectedon.png',height=40,width=40,mode='none')
            else:
                switchpng = switchColor(file='mainicons/interface/switchselectedoff.png',height=40,width=40,mode='none')
            self.switch.configure(image=switchpng)
            self.switch.image = switchpng
        def checkleave(event):
            parent.bind_all('<Button-1>',defocuswidget)
            self.widgetname.unbind_all('<Return>')
            self.widgetname.unbind_all('<space>')
            if self.state == True:
                switchpng = switchColor(file='mainicons/interface/switchon.png',height=40,width=40,mode='color')
            else:
                switchpng = switchColor(file='mainicons/interface/switchoff.png',height=40,width=40,mode='dynamic')
            self.switch.configure(image=switchpng)
            self.switch.image = switchpng


        #self.widgetname = Frame(self.parent,borderwidth=2,bg='red')
        self.widgetname = Frame(self.parent,takefocus=True,background=dynamicBackground())


        switchpng = switchColor(file='mainicons/interface/switchoff.png',height=40,width=40,mode='dynamic')
        self.switch = Label(self.widgetname,image=switchpng,bg=dynamicBackground())
        self.switch.image = switchpng

        self.switchtext = Label(self.parent,text=self.placeholder,font=mainfont,bg=dynamicBackground(),fg=dynamicForeground())

        self.switch.bind('<Button-1>',switchchangemode)
        self.switch.bind('<Enter>',checkenter)
        self.switch.bind('<Leave>',checkleave)
        self.widgetname.bind('<FocusIn>',checkenter)
        self.widgetname.bind('<FocusOut>',checkleave)

        self.switch.bind('<Enter>',checkenter)
        self.switch.bind('<Leave>',checkleave)
        self.switch.bind('<Button-1>',switchchangemode)

    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0):
        self.x = x
        self.y = y

        #self.widgetname.pack()
        self.widgetname.place(x=self.x,y=self.y,height=40,width=40)
        self.switch.place(x=0,y=0,height=40,width=40)
        self.switchtext.place(x=self.x+45,y=self.y,height=40)
        #self.checkplaceholder.pack()
        #self.checkplaceholder.place(x=100,y=0)
    def get(self):
        text = self.state.get()
        return(text)

class ComboBox(object):
    #Constructor de la clase
    def __init__(self,parent='*',state='normal',variables='*',index='0',action=None):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')

        if variables != '*':
            self.variables = variables
        else:
            raise TypeError('You must specify an array for the variables attribute.')


        self.height=32
        self.width=150
        self.state = state
        self.action = action

        def defocuswidget(event):
            try:
                parent.focus()
            except:
                pass

        def chevronfocusin(event):
            event.widget._nametowidget(event.widget.winfo_parent()).focus_force()
        def entryfocusin(event):
            parent.unbind_all('<Button-1>')
            def leavedropelement(event):
                event.widget.configure(bg=dynamicBackground())
            def enterdropelement(event):
                varselected = event.widget.cget('text')
                self.entry.icursor(0)
                self.entry.delete(0,'end')
                self.entry.insert(0,str(varselected))
                event.widget.configure(bg='#404040')
                event.widget.bind('<Leave>',leavedropelement)
            self.widgetname.place_forget()
            self.dropdown1 = Frame(self.parent,bg=dynamicBackground(),highlightthickness=1, highlightbackground="#838383",relief=FLAT)
            dropdownheight=5
            for i in range(len(self.variables)):
                a = Label(self.dropdown1,text=self.variables[i],anchor=W,bg=dynamicBackground(),fg=dynamicForeground(),font=mainfont)
                a.place(x=0,y=dropdownheight,width=self.width-2,height=30)
                a.bind('<Enter>',enterdropelement)
                dropdownheight=dropdownheight+30


            dropdownheight=dropdownheight+7
            self.dropdown1.place(x=self.x,y=self.y,height=dropdownheight,width=self.width)

        def entryfocusout(event):
            self.dropdown1.place_forget()
            self.widgetname.place(x=self.x,y=self.y,height=self.height,width=self.width)
            self.widgetname.configure(background='#939393')
            if self.entry.get() == '':
                self.entry.insert(0,str(self.placeholder))
            else:
                pass
            self.entry.configure(foreground='#939393',background=dynamicBackground())
            chevronimg = makeIcon(file='mainicons/interface/chevrondown.png',height=24,width=24,mode='manual',color='#939393')
            self.chevron.configure(image=chevronimg)
            self.chevron.image = chevronimg
            if self.action != None:
                self.action(self)

        def entryenter(event):
            parent.unbind_all('<Button-1>')
            if parent.focus_get() == self.entry:
                pass
            else:
                if getDarkModeState() == 0:
                    self.widgetname.configure(background=dynamicForeground())
                    self.entry.configure(foreground=dynamicForeground())
                    chevronimg = makeIcon(file='mainicons/interface/chevrondown.png',height=24,width=24,mode='dynamic')
                    self.chevron.configure(image=chevronimg)
                    self.chevron.image = chevronimg
                else:
                    self.widgetname.configure(background='#696969')
                    self.entry.configure(foreground='#696969')
                    chevronimg = makeIcon(file='mainicons/interface/chevrondown.png',height=24,width=24,mode='manual',color='#696969')
                    self.chevron.configure(image=chevronimg)
                    self.chevron.image = chevronimg
        def entryleave(event):
            parent.bind_all('<Button-1>',defocuswidget)
            if parent.focus_get() == self.entry:
                pass
            else:
                self.widgetname.configure(background='#939393')
                self.entry.configure(foreground='#939393')
                self.widgetname.configure(background='#939393')
                self.entry.configure(foreground='#696969')
                chevronimg = makeIcon(file='mainicons/interface/chevrondown.png',height=24,width=24,mode='manual',color='#939393')
                self.chevron.configure(image=chevronimg)
                self.chevron.image = chevronimg

        self.widgetname = Frame(self.parent,borderwidth='2',background='#939393',takefocus=True)


        self.entry = Entry(self.widgetname,state=self.state,background=dynamicBackground(),relief=FLAT,foreground='#939393',selectbackground=getAccentColor(),disabledbackground='#939393',disabledforeground=dynamicBackground(),font=mainfont,takefocus=False)

        self.entry.insert(0,str(self.variables[index]))

        chevronimg = makeIcon(file='mainicons/interface/chevrondown.png',height=24,width=24,mode='manual',color='#939393')

        self.chevron = Label(self.widgetname,image=chevronimg,bg=dynamicBackground())
        self.chevron.image = chevronimg


        self.widgetname.bind('<FocusIn>',entryfocusin)
        self.widgetname.bind('<FocusOut>',entryfocusout)
        self.chevron.bind('<Button-1>',chevronfocusin)

        self.widgetname.bind('<Enter>',entryenter)
        self.entry.bind('<Enter>',entryenter)
        self.chevron.bind('<Enter>',entryenter)
        self.widgetname.bind('>Leave',entryleave)
        self.entry.bind('<Leave>',entryleave)
        self.chevron.bind('<Leave>',entryleave)

    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0,width=150):
        self.x = x
        self.y = y
        self.width = width

        self.widgetname.place(x=self.x,y=self.y,height=self.height,width=self.width)
        self.entry.place(x=0,y=0,height=28,width=self.width-32)
        self.chevron.place(x=self.width-32,y=0,)

    def pack():
        pass
    def get(self):
        text = self.entry.get()
        return(text)

class SimpleLabel(object):
    pass

class HeaderLabel(object):
    pass

class RadioButton(object):
    def __init__(self,parent='*',text='',image='',state=False,variable='',value=''):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')
        self.text = text
        if state == True or state == False:
            self.state = state
        else:
            raise TypeError('The state of this widget must be a Boolean (True/False)')

        self.height=20

        self.image=image

        self.variable = variable
        self.value = value


        def defocuswidget(event):
            parent.focus()
        def radioselector(event):
            print('clicao'+self.value)
        def radioenter(event):
            print('entered'+self.value)
            self.widgetname.bind_all('<Button-1>',radioselector)
            self.radio.bind_all('<Button-1>',radioselector)
            self.textlabel.bind_all('<Button-1>',radioselector)
        def radioleave(event):
            print('left'+self.value)
            self.widgetname.unbind_all('<Button-1>')
            self.radio.unbind_all('<Button-1>')
            self.textlabel.unbind_all('<Button-1>')

        self.widgetname = Frame(self.parent,takefocus=True,background=dynamicBackground())

        self.radionew = Radiobutton(self.widgetname,text="One", variable=self.variable, value=self.value)

        if self.variable == self.value:
            radioimage = makeIcon(file='mainicons/interface/radiobuttonselected.png',height=20,width=20,mode='color',color='#939393')
        else:
            radioimage = makeIcon(file='mainicons/interface/radiobuttonunselected.png',height=20,width=20,mode='color',color='#939393')

        self.radio = Label(self.widgetname,image=radioimage,bg=dynamicBackground(),borderwidth=0)
        self.radio.image = radioimage

        if self.image != '':
            customimageimg = ImageTk.PhotoImage(file=self.image)
            self.customimage = Label(self.widgetname,image=customimageimg,borderwidth=0)
            self.customimage.image = customimageimg

        self.textlabel = Label(self.widgetname,text=self.text,font=mainfont,bg=dynamicBackground(),fg=dynamicForeground())

        self.widgetname.bind("<Enter>",radioenter)
        self.widgetname.bind("<Leave>", radioleave)

    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0):
        self.x = x
        self.y = y
        self.widgetname.place(x=self.x,y=self.y,height=20,width=300)
        self.radio.place(x=0,y=0)
        self.textlabel.place(x=30,height=20)
        if self.image != '':
            self.widgetname.place_configure(height=50,width=300)
            self.radio.place_configure(x=0,y=15)
            self.textlabel.place_configure(x=110,height=50)
            self.customimage.place(x=30,height=50)

class CommonButton(object):

    #Constructor de la clase
    def __init__(self,parent='*',text='',state='normal',command='',mode='dynamic'):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')


        self.height=32
        self.width=150
        self.state = state
        self.text = text
        self.command = command

        if mode != 'dynamic' or mode != 'color':
            self.mode = mode
        else:
            TypeError("Mode only can be 'dynamic' or 'color'.")

        def defocuswidget(event) :
            try:
                parent.focus()
            except:
                pass
        def buttonenter(event):
            parent.unbind_all('<Button-1>')
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#939393')
            else:
                self.widgetname.configure(background='#939393')
        def buttonleave(event):
            parent.bind_all('<Button-1>',defocuswidget)
            self.widgetname.configure(background='#6d6d6d')
        def buttonclick(event):
            parent.unbind_all('<Button-1>')
            self.widgetname.bind('<KeyRelease-Return>',buttonrelease)
            self.widgetname.bind('<KeyRelease-space>',buttonrelease)
            if getDarkModeState() == 0:
                self.buttoninside.configure(background='#939393')
                self.widgetname.configure(background='#939393')
            else:
                self.buttoninside.configure(background='#939393')
                self.widgetname.configure(background='#939393')
        def buttonrelease(event):
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#6d6d6d')
                self.buttoninside.configure(background='#6d6d6d')
            else:
                self.widgetname.configure(background='#c6c6c6')
                self.buttoninside.configure(background='#c6c6c6')
            if self.command != '':
                self.command()
            else:
                pass
        def buttonfocusin(event):
            parent.unbind_all('<Button-1>')
            self.widgetname.bind('<Return>',buttonclick)
            self.widgetname.bind('<space>',buttonclick)
            if getDarkModeState() == 0:
                self.widgetname.configure(background=dynamicForeground())
            else:
                self.widgetname.configure(background=dynamicForeground())
        def buttonfocusout(event):
            self.widgetname.unbind('<Return>')
            self.widgetname.unbind('<space>')
            self.widgetname.configure(background='#c6c6c6')

        self.widgetname = Frame(self.parent,borderwidth='0',takefocus=True)
        self.buttoninside = Label(self.widgetname,borderwidth='0',text=self.text,font=mainfont)

        if self.mode == 'dynamic':
            if getDarkModeState() == 0:
                self.widgetname.configure(bg='#6d6d6d')
                self.buttoninside.configure(bg='#6d6d6d',fg=dynamicForeground())
            else:
                self.widgetname.configure(bg='#c6c6c6')
                self.buttoninside.configure(bg='#c6c6c6',fg=dynamicForeground())
        else:
            self.widgetname.configure(bg=dynamicBackground())
            self.buttoninside.configure(bg=dynamicBackground(),fg=dynamicForeground())

        self.widgetname.bind('<Enter>',buttonenter)
        self.buttoninside.bind('<Enter>',buttonenter)

        self.widgetname.bind('<Leave>',buttonleave)
        self.buttoninside.bind('<Leave>',buttonleave)

        self.widgetname.bind('<Button-1>',buttonclick)
        self.buttoninside.bind('<Button-1>',buttonclick)

        self.widgetname.bind('<ButtonRelease-1>',buttonrelease)
        self.buttoninside.bind('<ButtonRelease-1>',buttonrelease)

        self.widgetname.bind('<FocusIn>',buttonfocusin)

        self.widgetname.bind('<FocusOut>',buttonfocusout)

    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0,width=100):
        self.x = x
        self.y = y
        self.width = width

        self.widgetname.place(x=self.x,y=self.y,height=self.height,width=self.width)
        self.buttoninside.place(x=2,y=2,height=self.height-4,width=self.width-4)

    def changeMode(mode):
        pass

class ColorButton(object):
    #Constructor de la clase
    def __init__(self,parent='*',text='',state='normal',command=''):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')


        self.height=32
        self.width=150
        self.state = state
        self.text = text
        self.command = command

        def defocuswidget(event) :
            try:
                parent.focus()
            except:
                pass
        def buttonenter(event):
            parent.unbind_all('<Button-1>')
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#939393')
            else:
                self.widgetname.configure(background='#939393')
        def buttonleave(event):
            parent.bind_all('<Button-1>',defocuswidget)
            self.widgetname.configure(background='#6d6d6d')
        def buttonclick(event):
            parent.unbind_all('<Button-1>')
            self.widgetname.bind('<KeyRelease-Return>',buttonrelease)
            self.widgetname.bind('<KeyRelease-space>',buttonrelease)
            if getDarkModeState() == 0:
                self.buttoninside.configure(background='#939393')
                self.widgetname.configure(background='#939393')
            else:
                self.buttoninside.configure(background='#939393')
                self.widgetname.configure(background='#939393')
        def buttonrelease(event):
            if getDarkModeState() == 0:
                self.widgetname.configure(background='#6d6d6d')
                self.buttoninside.configure(background='#6d6d6d')
            else:
                self.widgetname.configure(background='#c6c6c6')
                self.buttoninside.configure(background='#c6c6c6')
            if self.command != '':
                self.command()
            else:
                pass
        def buttonfocusin(event):
            parent.unbind_all('<Button-1>')
            self.widgetname.bind('<Return>',buttonclick)
            self.widgetname.bind('<space>',buttonclick)
            if getDarkModeState() == 0:
                self.widgetname.configure(background=dynamicForeground())
            else:
                self.widgetname.configure(background=dynamicForeground())
        def buttonfocusout(event):
            self.widgetname.unbind('<Return>')
            self.widgetname.unbind('<space>')
            self.widgetname.configure(background='#c6c6c6')

        self.widgetname = Frame(self.parent,borderwidth='0',background=getAccentColor(),takefocus=True)
        self.buttoninside = Label(self.widgetname,borderwidth='0',background=getAccentColor(),text=self.text,font=mainfont)

        if getDarkModeState() == 0:
            self.widgetname.configure(bg=getAccentColor())
            self.buttoninside.configure(bg=getAccentColor(),fg=dynamicForeground())

        self.widgetname.bind('<Enter>',buttonenter)
        self.buttoninside.bind('<Enter>',buttonenter)

        self.widgetname.bind('<Leave>',buttonleave)
        self.buttoninside.bind('<Leave>',buttonleave)

        self.widgetname.bind('<Button-1>',buttonclick)
        self.buttoninside.bind('<Button-1>',buttonclick)

        self.widgetname.bind('<ButtonRelease-1>',buttonrelease)
        self.buttoninside.bind('<ButtonRelease-1>',buttonrelease)

        self.widgetname.bind('<FocusIn>',buttonfocusin)

        self.widgetname.bind('<FocusOut>',buttonfocusout)

    #Método para mostrar el objeto en la interfaz
    def place(self,x=0,y=0,width=100):
        self.x = x
        self.y = y
        self.width = width

        self.widgetname.place(x=self.x,y=self.y,height=self.height,width=self.width)
        self.buttoninside.place(x=2,y=2,height=self.height-4,width=self.width-4)

    def pack():
        pass

class MainSectionLabel(object):
    def __init__(self,parent='*',widgetname='default',labelname='',labeldescription=' ',icon='*'):
        if parent != '*':
            self.parent = parent
        else:
            raise TypeError('You must specify a parent for this widget.')
        self.widgetname = widgetname
        self.labelname = labelname
        self.labeldescription = labeldescription
        self.icon = icon

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, bg, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,bg=bg)
        vscrollbar.config(command=canvas.yview)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas,bg=bg)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        a = Frame(self.interior,height=10,bg=dynamicBackground())
        a.pack()

        def canvasscroll(event):
            canvas.yview('scroll',int(-1*(event.delta/120)), "units")

        def _configure_canvas(event):
            a.configure(height=10)
            a.update()
            mylist = interior.winfo_children()
            for i in mylist:
                lasty=i.winfo_height()+i.winfo_y()
            a.configure(height=lasty+150)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

            if canvas.winfo_height()<lasty:
                vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
                canvas.config(scrollregion=(0,0,0,lasty))
                canvas.bind_all("<MouseWheel>", canvasscroll)
            else:
                canvas.unbind_all("<MouseWheel>")
                try:
                    vscrollbar.pack_forget()
                except:
                    pass
                canvas.config(scrollregion=(0,0,0,0))


        canvas.bind('<Configure>', _configure_canvas)

class MainIconMenu(object):
    def __init__(self,parent='*',title='Main Title',description='Main description for the window.', state='normal'):

        global activeresizestate
        activeresizestate = 0

        global mainmenustateresizevariable

        mainmenustateresizevariable = self


        if parent != '*':
            self.parent=parent
        else:
            raise TypeError('You must specify a parent for this widget.')

        self.title=title
        self.description=description

        self.frame = Frame(self.parent,bg=dynamicBackground(),width=self.parent.winfo_width(),height=self.parent.winfo_height(),name='maincontainer')
        self.frametitle = Label(self.frame,text=self.title,bg=dynamicBackground(),fg=dynamicForeground(),font=titlelightfont)
        self.framedescription = Label(self.frame,text=self.description, bg=dynamicBackground(),fg=dynamicForeground(),font=mainfont)
        self.iconframe = VerticalScrolledFrame(self.frame,bg=dynamicBackground())

        self.elementnumber = 0


        self.iconimage = []

    def enableresize(self):
        def resizeevent(event):
            global activeresizestate
            width=self.parent.winfo_width()
            height=self.parent.winfo_height()
            self.frame.configure(width=width,height=height)
            self.frametitle.place_configure(width=width)
            self.framedescription.place_configure(width=width)
            mylist=['1','2','3','4','5','6','7','8','9','10']
            if width < 370:
                if activeresizestate != 1:
                    activeresizestate = 1
                    self.iconframe.place_configure(x=0,width=width,height=height-140)
                    for i in (self.iconframe.interior.winfo_children()):
                        if i.winfo_name() in mylist:
                            i.winfo_children()[2].configure(wraplength=245)
                else:
                    self.iconframe.place_configure(x=0,width=width,height=height-140)
            elif width >= 370 and width < 480:
                if activeresizestate !=2:
                    activeresizestate = 2
                    self.iconframe.place_configure(x=0,width=width,height=height-140)
                    for i in (self.iconframe.interior.winfo_children()):
                        if i.winfo_name() in mylist:
                            i.winfo_children()[2].configure(wraplength=300)
                else:
                    self.iconframe.place_configure(width=width,height=height-140)
            elif width >= 480 and width < 600:
                if activeresizestate != 3:
                    activeresizestate = 3
                    self.iconframe.place_configure(x=0,width=width,height=height-140)
                    for i in (self.iconframe.interior.winfo_children()):
                        if i.winfo_name() in mylist:
                            i.place_configure(relx=0,height=90,relwidth=1,rely=0,relheight=0)
                        if i.winfo_name() == '1':
                            i.place_configure(y=10)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '2':
                            i.place_configure(y=90)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '3':
                            i.place_configure(y=180)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '4':
                            i.place_configure(y=270)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '5':
                            i.place_configure(y=360)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '6':
                            i.place_configure(y=450)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '7':
                            i.place_configure(y=540)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '8':
                            i.place_configure(y=630)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '9':
                            i.place_configure(y=720)
                            i.winfo_children()[2].configure(wraplength=400)
                        if i.winfo_name() == '10':
                            i.place_configure(y=810)
                            i.winfo_children()[2].configure(wraplength=400)
                else:
                    self.iconframe.place_configure(width=width,height=height-140)
            elif width >= 600 and width < 850:
                if activeresizestate != 4:
                    activeresizestate = 4
                    self.iconframe.place_configure(x=0,width=width,height=height-140)
                    for i in (self.iconframe.interior.winfo_children()):
                        if i.winfo_name() in mylist:
                            i.place_configure(relwidth=0.45,height=100)
                        if i.winfo_name() == '1':
                            i.place_configure(relx=0.033,y=10)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '2':
                            i.place_configure(relx=0.516,y=10)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '3':
                            i.place_configure(relx=0.033,y=120)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '4':
                            i.place_configure(relx=0.516,y=120)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '5':
                            i.place_configure(relx=0.033,y=230)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '6':
                            i.place_configure(relx=0.516,y=230)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '7':
                            i.place_configure(relx=0.033,y=340)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '8':
                            i.place_configure(relx=0.516,y=340)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '9':
                            i.place_configure(relx=0.033,y=450)
                            i.winfo_children()[2].configure(wraplength=180)
                        if i.winfo_name() == '10':
                            i.place_configure(relx=0.516,y=450)
                            i.winfo_children()[2].configure(wraplength=180)
                else:
                    self.iconframe.place_configure(width=width,height=height-140)
            elif width >= 850 and width < 1200:
                if activeresizestate != 5:
                    activeresizestate = 5
                    self.iconframe.place_configure(x=0,width=width,height=height-140)
                    for i in (self.iconframe.interior.winfo_children()):
                        if i.winfo_name() in mylist:
                            i.place_configure(relwidth=0.30,height=100)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '1':
                            i.place_configure(relx=0.025,y=10)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '2':
                            i.place_configure(relx=0.350,y=10)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '3':
                            i.place_configure(relx=0.675,y=10)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '4':
                            i.place_configure(relx=0.025,y=120)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '5':
                            i.place_configure(relx=0.350,y=120)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '6':
                            i.place_configure(relx=0.675,y=120)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '7':
                            i.place_configure(relx=0.025,y=230)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '8':
                            i.place_configure(relx=0.350,y=230)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '9':
                            i.place_configure(relx=0.675,y=230)
                            i.winfo_children()[2].configure(wraplength=170)
                        if i.winfo_name() == '10':
                            i.place_configure(relx=0.025,y=340)
                            i.winfo_children()[2].configure(wraplength=170)
                else:
                    self.iconframe.place_configure(width=width,height=height-140)
            elif width >= 1200:
                if activeresizestate != 6:
                    activeresizestate = 6
                    self.iconframe.place_configure(x=(width/2)-600,y=100,width=1200,height=height-140)
                    for i in (self.iconframe.interior.winfo_children()):
                        if i.winfo_name() in mylist:
                            i.place_configure(relwidth=0.225,height=100)
                        if i.winfo_name() == '1':
                            i.place_configure(relx=0.020,y=10)
                        if i.winfo_name() == '2':
                            i.place_configure(relx=0.265,y=10)
                        if i.winfo_name() == '3':
                            i.place_configure(relx=0.510,y=10)
                        if i.winfo_name() == '4':
                            i.place_configure(relx=0.755,y=10)
                        if i.winfo_name() == '5':
                            i.place_configure(relx=0.020,y=120)
                        if i.winfo_name() == '6':
                            i.place_configure(relx=0.265,y=120)
                        if i.winfo_name() == '7':
                            i.place_configure(relx=0.510,y=120)
                        if i.winfo_name() == '8':
                            i.place_configure(relx=0.755,y=120)
                        if i.winfo_name() == '9':
                            i.place_configure(relx=0.020,y=230)
                        if i.winfo_name() == '10':
                            i.place_configure(relx=0.265,y=230)
                else:
                    self.iconframe.place_configure(x=(width/2)-600,width=1200,height=height-140)
        self.parent.bind("<Configure>",resizeevent)

    def pack(self):
        self.frame.pack()
        self.enableresize()
        self.frametitle.place(x=0,y=20,width=self.parent.winfo_width())
        self.framedescription.place(x=0,y=50,width=self.parent.winfo_width())
        self.iconframe.place(x=0,y=100,width=self.parent.winfo_width(),height=660)

    def addElement(self,title='Element title',description='Element description.',icon='*',command='*'):
        def applyConditions(element):
            if int(element.winfo_name()) == 0:
                raise Exception('Element not managed correctly.')
            elif int(element.winfo_name()) == 1:
                element.place(relx=0.025,y=10,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 2:
                element.place(relx=0.350,y=10,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 3:
                element.place(relx=0.675,y=10,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 4:
                element.place(relx=0.025,y=120,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 5:
                element.place(relx=0.350,y=120,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 6:
                element.place(relx=0.675,y=120,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 7:
                element.place(relx=0.025,y=230,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 8:
                element.place(relx=0.350,y=230,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 9:
                element.place(relx=0.675,y=230,height=100,relwidth=0.30)
            elif int(element.winfo_name()) == 10:
                element.place(relx=0.025,y=340,height=100,relwidth=0.30)
            elementicon.place(x=10,width=60,height=60,y=10)
            elementtitle.place(x=75,y=10)
            elementdescription.place(x=75,y=40)
        def elementclick(event):
            if command != '*':
                element.configure(bg='#5d5d5d')
                elementicon.configure(bg='#5d5d5d')
                elementtitle.configure(bg='#5d5d5d')
                elementdescription.configure(bg='#5d5d5d')
                for i in self.parent.winfo_children():
                    if i.winfo_name() == 'maincontainer':
                        i.pack_forget()
                        command(self.parent)
            else:
                pass
        def elementrelease(event):
            element.configure(bg='#181818')
            elementicon.configure(bg='#181818')
            elementtitle.configure(bg='#181818')
            elementdescription.configure(bg='#181818')
        def elemententer(event):
            element.configure(bg='#181818')
            elementicon.configure(bg='#181818')
            elementtitle.configure(bg='#181818')
            elementdescription.configure(bg='#181818')
            element.bind("<Button-1>",elementclick)
            elementicon.bind("<Button-1>",elementclick)
            elementtitle.bind("<Button-1>",elementclick)
            elementdescription.bind("<Button-1>",elementclick)
            element.bind("<ButtonRelease-1>",elementrelease)
            elementicon.bind("<ButtonRelease-1>",elementrelease)
            elementtitle.bind("<ButtonRelease-1>",elementrelease)
            elementdescription.bind("<ButtonRelease-1>",elementrelease)
        def elementleave(event):
            element.configure(bg=dynamicBackground())
            elementicon.configure(bg=dynamicBackground())
            elementtitle.configure(bg=dynamicBackground())
            elementdescription.configure(bg=dynamicBackground())
            element.unbind("<Button-1>")
            elementicon.unbind("<Button-1>")
            elementtitle.unbind("<Button-1>")
            elementdescription.unbind("<Button-1>")
        if self.elementnumber != 10:
            self.elementnumber = self.elementnumber + 1
        else:
            raise Exception("The maximum number of elements permitted is 10. We're working to upgrade this feature.")
        element = Frame(self.iconframe.interior,bg=dynamicBackground(),name=str(self.elementnumber))
        if icon != '*':
            self.iconimage.append(makeIcon(file=icon,height=60,width=60,mode='color'))
            elementicon = Label(element,bg=dynamicBackground(),image=self.iconimage[-1],name='icon')
        else:
            elementicon = Label(element,bg=dynamicBackground(),name='icon')
        elementtitle = Label(element,text=title,bg=dynamicBackground(),fg=dynamicForeground(),font=mainfont,name='title')
        elementdescription =  Label(element,text=description,bg=dynamicBackground(),fg=dynamicForeground(),font=subdescfont,name='description',wraplength=155,justify=LEFT)

        applyConditions(element)

        element.bind("<Enter>",elemententer)
        element.bind("<Leave>",elementleave)

class LeftSideBar(object):
    def __init__(self,parent='*',title='Main Title', state='normal',icon='*',backtext='Back to Main Menu'):

        global activeresizestate
        activeresizestate = 0

        global subpanels
        subpanels = []

        global activepanel
        activepanel = 'sp-1'

        self.elementlist = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']

        if parent != '*':
            self.parent=parent
        else:
            raise TypeError('You must specify a parent for this widget.')
        self.title=title
        self.iconimage = []
        self.backtext = backtext

        def backclick(event):
            self.backtitle.configure(bg='#5d5d5d')
            self.upsideframe.configure(bg='#5d5d5d')
            self.titleicon.configure(bg='#5d5d5d')
        def backrelease(event):
            for i in self.parent.winfo_children():
                if i.winfo_name() != 'maincontainer':
                    i.destroy()
                else:
                    global mainmenustateresizevariable
                    mainmenustateresizevariable.enableresize()
                    i.pack()
        def backenter(event):
            self.backtitle.configure(bg='#181818')
            self.upsideframe.configure(bg='#181818')
            self.titleicon.configure(bg='#181818')
            self.backtitle.bind("<Button-1>",backclick)
            self.titleicon.bind("<Button-1>",backclick)
            self.upsideframe.bind("<ButtonRelease-1>",backrelease)
            self.titleicon.bind("<ButtonRelease-1>",backrelease)
            self.backtitle.bind("<ButtonRelease-1>",backrelease)
        def backleave(event):
            self.backtitle.configure(bg=dynamicBackground())
            self.upsideframe.configure(bg=dynamicBackground())
            self.titleicon.configure(bg=dynamicBackground())
            self.backtitle.unbind("<Button-1>")
            self.titleicon.unbind("<Button-1>")
            self.upsideframe.unbind("<ButtonRelease-1>")


        self.frame = Frame(self.parent,bg=dynamicBackground(),width=self.parent.winfo_width(),height=self.parent.winfo_height())
        self.upsideframe = Frame(self.frame,bg=dynamicBackground(),width=self.parent.winfo_width(),height=200)
        if icon != '*':
            self.iconimage.append(makeIcon(file=icon,height=30,width=30,mode='color'))
            self.titleicon = Label(self.upsideframe, bg=dynamicBackground(), image=self.iconimage[-1], name='icon')
        else:
            self.titleicon = Label(self.upsideframe, bg=dynamicBackground(), name='icon')
        self.backtitle = Label(self.upsideframe,text=self.backtext,bg=dynamicBackground(),fg=dynamicForeground(),font=titlefont15)#Back to Main Menu
        self.frametitle = Label(self.frame,text=self.title,bg=dynamicBackground(),fg=dynamicForeground(),font=titlefont13bold)

        self.iconframe = VerticalScrolledFrame(self.frame,bg=dynamicBackground())

        self.elementnumber = 0

        self.upsideframe.bind("<Enter>",backenter)
        self.upsideframe.bind("<Leave>",backleave)

    def pack(self):
        self.frame.pack(anchor=NW)
        width=self.parent.winfo_width()
        height=self.parent.winfo_height()

        for i in (self.iconframe.interior.winfo_children()):
            if i.winfo_name() in self.elementlist:
                i.place_configure(relx=0,height=50,relwidth=1,rely=0,relheight=0)
            if i.winfo_name() == '1':
                i.place_configure(y=0)
            if i.winfo_name() == '2':
                i.place_configure(y=50)
            if i.winfo_name() == '3':
                i.place_configure(y=100)
            if i.winfo_name() == '4':
                i.place_configure(y=150)
            if i.winfo_name() == '5':
                i.place_configure(y=200)
            if i.winfo_name() == '6':
                i.place_configure(y=250)
            if i.winfo_name() == '7':
                i.place_configure(y=300)
            if i.winfo_name() == '8':
                i.place_configure(y=350)
            if i.winfo_name() == '9':
                i.place_configure(y=400)
            if i.winfo_name() == '10':
                i.place_configure(y=450)
            if i.winfo_name() == '11':
                i.place_configure(y=500)
            if i.winfo_name() == '12':
                i.place_configure(y=550)
            if i.winfo_name() == '13':
                i.place_configure(y=600)
            if i.winfo_name() == '14':
                i.place_configure(y=650)
            if i.winfo_name() == '15':
                i.place_configure(y=700)
            if i.winfo_name() == '16':
                i.place_configure(y=750)
            if i.winfo_name() == '17':
                i.place_configure(y=800)
            if i.winfo_name() == '18':
                i.place_configure(y=850)
            if i.winfo_name() == '19':
                i.place_configure(y=900)
            if i.winfo_name() == '20':
                i.place_configure(y=950)
            if i.winfo_name() == '21':
                i.place_configure(y=1000)
            if i.winfo_name() == '22':
                i.place_configure(y=1050)
            if i.winfo_name() == '23':
                i.place_configure(y=1100)
            if i.winfo_name() == '24':
                i.place_configure(y=1150)
            if i.winfo_name() == '25':
                i.place_configure(y=1200)

        self.upsideframe.place(x=0,y=0,height=60)
        self.titleicon.place(x=10,y=10,height=40,width=30)
        self.backtitle.place(x=50,y=10,height=40)
        self.frametitle.place(x=10,y=60,height=40)
        self.iconframe.place(x=0,y=100,width=300,height=height-140)

    def addElement(self,title='Element title',icon='*',panelload='*'):
        def applyConditions(element):
            if int(element.winfo_name()) == 0:
                raise Exception('Element not managed correctly.')
            element.place(relx=0,height=50,relwidth=1,rely=0,relheight=0)
            elementicon.place(x=10,width=30,height=30,y=10)
            elementtitle.place(x=45,y=10)
            for i in (self.iconframe.interior.winfo_children()):
                if i.winfo_name() in self.elementlist:
                    i.place_configure(relx=0,height=50,relwidth=1,rely=0,relheight=0)
                if i.winfo_name() == '1':
                    i.place_configure(y=0)
                if i.winfo_name() == '2':
                    i.place_configure(y=50)
                if i.winfo_name() == '3':
                    i.place_configure(y=100)
                if i.winfo_name() == '4':
                    i.place_configure(y=150)
                if i.winfo_name() == '5':
                    i.place_configure(y=200)
                if i.winfo_name() == '6':
                    i.place_configure(y=250)
                if i.winfo_name() == '7':
                    i.place_configure(y=300)
                if i.winfo_name() == '8':
                    i.place_configure(y=350)
                if i.winfo_name() == '9':
                    i.place_configure(y=400)
                if i.winfo_name() == '10':
                    i.place_configure(y=450)
                if i.winfo_name() == '11':
                    i.place_configure(y=500)
                if i.winfo_name() == '12':
                    i.place_configure(y=550)
                if i.winfo_name() == '13':
                    i.place_configure(y=600)
                if i.winfo_name() == '14':
                    i.place_configure(y=650)
                if i.winfo_name() == '15':
                    i.place_configure(y=700)
                if i.winfo_name() == '16':
                    i.place_configure(y=750)
                if i.winfo_name() == '17':
                    i.place_configure(y=800)
                if i.winfo_name() == '18':
                    i.place_configure(y=850)
                if i.winfo_name() == '19':
                    i.place_configure(y=900)
                if i.winfo_name() == '20':
                    i.place_configure(y=950)
                if i.winfo_name() == '21':
                    i.place_configure(y=1000)
                if i.winfo_name() == '22':
                    i.place_configure(y=1050)
                if i.winfo_name() == '23':
                    i.place_configure(y=1100)
                if i.winfo_name() == '24':
                    i.place_configure(y=1150)
                if i.winfo_name() == '25':
                    i.place_configure(y=1200)

            global activepanel
            global subpanels

            for i in self.parent.winfo_children():
                if i.winfo_name() in subpanels:
                    if str(i.winfo_name()) == activepanel:
                        if str(activepanel) == str(panelload.panelid):
                            panelload.pack()
                            elementselectionindicator.place(x=0,y=13,width=5,height=24)
        def elementclick(event):
            if panelload != '*':
                global activepanel
                global subpanels

                self.parent.geometry(str(self.parent.winfo_width()+1)+'x'+str(self.parent.winfo_height()))

                element.configure(bg='#5d5d5d')
                elementicon.configure(bg='#5d5d5d')
                elementtitle.configure(bg='#5d5d5d')

                a=panelload

                for i in self.parent.winfo_children():
                    if i.winfo_name() in subpanels:
                        if panelload.panelid == str(i.winfo_name()) and panelload.panelid == activepanel:
                            pass
                        elif panelload.panelid == str(i.winfo_name()) and panelload.panelid != activepanel:
                            panelload.pack()
                            activepanel = panelload.panelid
                            elementselectionindicator.place(x=0,y=13,width=5,height=24)
                        elif panelload.panelid != str(i.winfo_name()):
                            a.disableresize()
                            i.place_forget()
                for i in self.iconframe.interior.winfo_children():
                    if str(i.winfo_name()) in self.elementlist:
                        if str(i.winfo_name()) != element.winfo_name():
                            for n in i.winfo_children():
                                if str(n.winfo_name()) == 'ind':
                                    n.place_forget()
        def elementrelease(event):
            element.configure(bg='#181818')
            elementicon.configure(bg='#181818')
            elementtitle.configure(bg='#181818')
        def elemententer(event):
            element.configure(bg='#181818')
            elementicon.configure(bg='#181818')
            elementtitle.configure(bg='#181818')
            element.bind("<Button-1>",elementclick)
            elementicon.bind("<Button-1>",elementclick)
            elementtitle.bind("<Button-1>",elementclick)
            element.bind("<ButtonRelease-1>",elementrelease)
            elementicon.bind("<ButtonRelease-1>",elementrelease)
            elementtitle.bind("<ButtonRelease-1>",elementrelease)
        def elementleave(event):
            element.configure(bg=dynamicBackground())
            elementicon.configure(bg=dynamicBackground())
            elementtitle.configure(bg=dynamicBackground())
            element.unbind("<Button-1>")
            elementicon.unbind("<Button-1>")
            elementtitle.unbind("<Button-1>")
        if self.elementnumber != 25:
            self.elementnumber = self.elementnumber + 1
        else:
            raise Exception("The maximum number of elements permitted are 25. We're working to upgrade this feature.")
        element = Frame(self.iconframe.interior,bg=dynamicBackground(),name=str(self.elementnumber))
        elementselectionindicator = Frame(element, bg=getAccentColor(),name='ind')
        if icon != '*':
            self.iconimage.append(makeIcon(file=icon,height=20,width=20,mode='dynamic'))
            elementicon = Label(element,bg=dynamicBackground(),image=self.iconimage[-1],name='icon')
        else:
            elementicon = Label(element,bg=dynamicBackground(),name='icon')
        elementtitle = Label(element,text=title,bg=dynamicBackground(),fg=dynamicForeground(),font=mainfont,name='title')

        applyConditions(element)

        element.bind("<Enter>",elemententer)
        element.bind("<Leave>",elementleave)

class UtilityPanel(object):
    def __init__(self,parent='*',title='Main Title',state='normal',bg='red'):
        super().__init__()
        if parent != '*':
            self.parent=parent
        else:
            raise TypeError('You must specify a parent for this widget.')
        self.title=title

        global subpanels

        if len(subpanels) == 0:
            self.panelid = 'sp-1'
            subpanels.append('sp-1')
        else:
            self.panelid = 'sp-'+str(int(subpanels[-1].split('-')[1])+1)
            subpanels.append(self.panelid)

        self.panel = VerticalScrolledFrame(self.parent,bg=bg,height=200,name=self.panelid)

    def enableresize(self):
        def resizeevent(event):
            self.panel.place_configure(x=300,width=self.parent.winfo_width()-300,relheight=1)

        self.parent.bind('<Configure>',resizeevent)

    def disableresize(self):
        self.parent.unbind_all('<Configure>')


    def __call__(self):
        return(self.panel.interior)

    def pack(self):
        #self.panel.pack(expand=True,side=top)
        self.enableresize()
        self.panel.place(x=300,width=self.parent.winfo_width()-300,relheight=1)
