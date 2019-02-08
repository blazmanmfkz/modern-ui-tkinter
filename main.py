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
# ---------------------------------------Main file--------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------





import mainfunctions as fn
from interface import *
import win32print
import serial



#Load parameters
def loadParameters():
    file = open('preferences/myprefs.json','r',encoding='utf-8')
    data = str(file.read())
    file.close()

    global myprefs
    # Parse JSON into an object with attributes corresponding to dict keys.
    myprefs = fn.Preferences(json.loads(data))

loadParameters()

if myprefs.languageselected == 'ESP':
    with open('languages/spanish.blf', 'r', encoding='utf-8') as languagefile:
        languagecontents = languagefile.read()
    exec(languagecontents)
elif myprefs.languageselected == 'ENG':
    with open('languages/english.blf', 'r', encoding='utf-8') as languagefile:
        languagecontents = languagefile.read()
    exec(languagecontents)
else:
    pass

def initmainwindow():
    #on closing function
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            a = myprefs.dumpjson()
            file = open('preferences/myprefs.json','r+',encoding='utf-8')
            file.write(a)
            file.close()
            mainwindow.destroy()

    # Function that initialise the main window
    mainwindow = tk.Tk()
    mainwindow.resizable(1, 1)
    mainwindow.title('Resizable Icons')
    mainwindoww = 900
    mainwindowh = 600
    mainwindowws = mainwindow.winfo_screenwidth()
    mainwindowhs = mainwindow.winfo_screenheight()
    x = (mainwindowws / 2) - (mainwindoww / 2)
    y = (mainwindowhs / 2) - (mainwindowh / 2)
    mainwindow.geometry('%dx%d+%d+%d' % (mainwindoww, mainwindowh, x, y))
    mainwindow.minsize(500, 600)
    style = ThemedStyle(mainwindow)
    style.set_theme("radiance")
    if getDarkModeState() == 0:
        mainwindow.configure(background='#000000')
    else:
        mainwindow.configure(background='#ffffff')

    class boosMainMenu:
        def __init__(self, parent):
            # Production Manager
            # Boos Technical Lighting S.L.
            menu = MainIconMenu(parent, title=mtstring1, description=mdstring1)
            menu.pack()

            class userSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring1,
                                                  icon='mainicons/back.png')  # User

                    menu.pack()

                    class panel1():
                        panel1 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm1string1, panelload=panel1,
                                                   icon='mainicons/edituser.png')  # Account info

                        element1 = Label(panel1(), text='Bienvenido al panel de usuario', font=mainfontbold,
                                         bg=dynamicBackground(), fg=dynamicForeground())
                        element1.place(x=10, y=10)
                        element2 = Label(panel1(),
                                         text="En este panel podrás ver tu información personal como empleado dentro de la empresa y modificar algunas opciones.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=40)
                        element3 = Label(panel1(), text='Nombre:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element3.place(x=10, y=100)
                        element4 = TextEntry(panel1(), text=myprefs.username)
                        element4.place(x=13, y=130, width=250)

                        element5 = Label(panel1(), text='Apellidos:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element5.place(x=310, y=100)
                        element6 = TextEntry(panel1(), text=myprefs.usersurname)
                        element6.place(x=313, y=130, width=250)

                        element3 = Label(panel1(), text='Número único de empleado:', font=mainfont,
                                         bg=dynamicBackground(), fg=dynamicForeground())
                        element3.place(x=10, y=200)
                        element4 = TextEntry(panel1(), text=myprefs.usernumber)
                        element4.place(x=13, y=230, width=250)

                        element3 = Label(panel1(), text='Correo electrónico:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element3.place(x=10, y=300)
                        element4 = TextEntry(panel1(), text=myprefs.useremail)
                        element4.place(x=13, y=330, width=250)

                        element3 = Label(panel1(), text='Password:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element3.place(x=310, y=300)
                        element4 = TextEntry(panel1(), text=myprefs.userpassword, show='*')
                        element4.place(x=313, y=330, width=250)

                    class panel2():
                        panel2 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm1string2, panelload=panel2,
                                                   icon='mainicons/more.png')  # More options
                        element1 = Label(panel2(), text='Otras opciones', font=mainfontbold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element1.place(x=10, y=10)
                        element2 = Label(panel2(),
                                         text="Por el momento, este panel no cuenta con opciones con las que poder interactuar.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=40)

            class orderTestingSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring2,
                                                  icon='mainicons/back.png')  # Order testing

                    menu.pack()

                    class panel1():

                        global testrunning
                        testrunning = False

                        def demotest():
                            orden = self.element1.get()
                            global testrunning

                            def fun():
                                global testrunning
                                imgx = makeIcon(file='mainicons/interface/radialindicator.png', height=150, width=150,
                                                mode='manual', color='#939393')
                                self.element9.config(image=imgx)
                                self.element9.image = imgx
                                self.indicator9.config(text='reading')
                                self.element10.config(image=imgx)
                                self.element10.image = imgx
                                self.indicator10.config(text='ready')
                                self.element11.config(image=imgx)
                                self.element11.image = imgx
                                self.indicator11.config(text='ready')
                                self.element12.config(image=imgx)
                                self.element12.image = imgx
                                self.indicator12.config(text='ready')
                                for i in range(0, 101):
                                    self.pbarprog.config(text=str(i) + '%')
                                    self.pbarfilled.place(x=0, y=0, relwidth=i / 100, relheight=1)
                                    if testrunning == True:
                                        if i == 1:
                                            print('Starting GROUND test.')
                                            time.sleep(1)
                                        if i == 7:
                                            print('Reading GROUND results...')
                                            self.indicator9.config(text='reading')
                                            time.sleep(4)
                                        elif i == 10:
                                            print('GROUND test is OK.\n\n')
                                            self.indicator9.config(text='ok')
                                            img9 = makeIcon(file='mainicons/interface/radialindicator.png', height=150,
                                                            width=150, mode='manual', color='#088116')
                                            self.element9.config(image=img9)
                                            self.element9.image = img9
                                            time.sleep(3)
                                            print('Starting ISOLATE test.')
                                        elif i == 20:
                                            print('Reading ISOLATE results...')
                                            self.indicator10.config(text='reading')
                                            time.sleep(5)
                                        elif i == 31:
                                            print('ISOLATE test is OK.\n\n')
                                            self.indicator10.config(text='ok')
                                            img10 = makeIcon(file='mainicons/interface/radialindicator.png', height=150,
                                                             width=150, mode='manual', color='#088116')
                                            self.element10.config(image=img10)
                                            self.element10.image = img10
                                            time.sleep(7)
                                        elif i == 50:
                                            print('Starting Driver programming phase...')
                                            print('Put the Simpleset antenna near to the driver.')
                                            self.indicator11.config(text='action')
                                            time.sleep(5)
                                        elif i == 51:
                                            print('Writing program to the driver.')
                                            self.indicator11.config(text='writing')
                                            time.sleep(10)
                                        elif i == 75:
                                            print('Driver programmed correctly.\n\n')
                                            self.indicator11.config(text='ok')
                                            img11 = makeIcon(file='mainicons/interface/radialindicator.png', height=150,
                                                             width=150, mode='manual', color='#088116')
                                            self.element11.config(image=img11)
                                            self.element11.image = img11
                                            time.sleep(10)
                                        elif i == 76:
                                            print('Starting FUNCTION test.')
                                            print('Reading power consumption results...')
                                            self.indicator12.config(text='reading')
                                            time.sleep(5)
                                        elif i == 90:
                                            print('The power consumption of the luminary is OK.\n\n')
                                            self.indicator12.config(text='49W')
                                            img12 = makeIcon(file='mainicons/interface/radialindicator.png', height=150,
                                                             width=150, mode='manual', color='#088116')
                                            self.element12.config(image=img12)
                                            self.element12.image = img12
                                            print('The Luminary is correctly tested.\n\n\n\n')
                                    else:
                                        print('Function cancelled')
                                        imgx = makeIcon(file='mainicons/interface/radialindicator.png', height=150,
                                                        width=150, mode='manual', color='#313131')
                                        self.element9.config(image=imgx)
                                        self.element9.image = imgx
                                        self.indicator9.config(text='ready')
                                        self.element10.config(image=imgx)
                                        self.element10.image = imgx
                                        self.indicator10.config(text='ready')
                                        self.element11.config(image=imgx)
                                        self.element11.image = imgx
                                        self.indicator11.config(text='ready')
                                        self.element12.config(image=imgx)
                                        self.element12.image = imgx
                                        self.indicator12.config(text='ready')
                                        return

                                    time.sleep(.060)
                                testrunning = False

                            if orden == 'Insert order number here':
                                pass
                            else:
                                if testrunning == False:
                                    testrunning = True
                                    print('Starting to test order: ' + str(orden))
                                    t = threading.Thread(target=fun)
                                    t.start()
                                else:
                                    print('El test está corriendo')

                        def stopdemotest():
                            global testrunning
                            if testrunning == True:
                                testrunning = False
                            else:
                                pass

                        def validatedata():
                            actualluminary = fn.validateData(self,
                                                             self.element1.get())

                        def starttest():
                            fn.starttest(self, 'a')

                        mainwindoww = 1200
                        mainwindowh = 800
                        mainwindowws = mainwindow.winfo_screenwidth()
                        mainwindowhs = mainwindow.winfo_screenheight()
                        x = (mainwindowws / 2) - (mainwindoww / 2)
                        y = (mainwindowhs / 2) - (mainwindowh / 2)
                        mainwindow.geometry('%dx%d+%d+%d' % (mainwindoww, mainwindowh, x, y))

                        panel1 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm2string1, panelload=panel1,
                                                   icon='mainicons/dali.png')  # Configurator testing

                        element0 = Label(panel1(), text='Order testing', font=titlebold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element0.place(x=10, y=10)

                        self.element1 = TextEntry(panel1(), placeholder='Insert order number here')
                        self.element1.place(x=10, y=70, width=250)

                        element2 = CommonButton(panel1(), text='Validate', command=validatedata)
                        element2.place(x=270, y=70)

                        element3a = Frame(panel1(), bg=getAccentColor())
                        element3a.place(x=10, y=130, width=230, height=230)

                        element3 = Label(element3a, text='Order data', font=titlefont15bold, bg=getAccentColor(),
                                         fg=dynamicForeground())
                        element3.place(x=10, y=10)

                        ordertext = '#:\nState:\nQuantity:\nTest to realize:'
                        self.element4 = Text(element3a, font=mainfont, borderwidth=0, bg=getAccentColor(),
                                             fg=dynamicForeground())
                        self.element4.insert(1.0, ordertext)
                        self.element4.config(state=DISABLED)
                        self.element4.place(x=10, y=60)

                        element5a = Frame(panel1(), bg=getAccentColor())
                        element5a.place(x=260, y=130, width=480, height=230)

                        element5 = Label(element5a, text='Luminary data', font=titlefont15bold, bg=getAccentColor(),
                                         fg=dynamicForeground())
                        element5.place(x=10, y=10)

                        luminarytext = 'Code:\nProgram:\nLed number:\nOptic:\nClass:\nPower consumption:'
                        luminarytext2 = 'Dimming:\nDimming level:\nPhotocell:\nCLO:\nLed Flux:\nLed Color:'
                        self.element6 = Text(element5a, font=mainfont, bg=getAccentColor(), borderwidth=0,
                                             fg=dynamicForeground())
                        self.element6.place(x=10, y=60)
                        self.element6.insert(1.0, luminarytext)
                        self.element6.config(state=DISABLED)
                        self.element7 = Text(element5a, font=mainfont, bg=getAccentColor(), borderwidth=0,
                                             fg=dynamicForeground())
                        self.element7.insert(1.0, luminarytext2)
                        self.element7.config(state=DISABLED)
                        self.element7.place(x=320, y=60)

                        element8 = Label(panel1(), text='Progress', font=titlefont15bold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element8.place(x=10, y=380)

                        img9 = makeIcon(file='mainicons/interface/radialindicator.png', height=150, width=150,
                                        mode='manual', color='#313131')
                        self.element9 = Label(panel1(), image=img9, bg=dynamicBackground())
                        self.element9.image = img9
                        self.element9.place(x=10, y=430)
                        self.indicator9 = Label(panel1(), text='ready', font=titlefontbig, bg=dynamicBackground(),
                                                fg=dynamicForeground())
                        self.indicator9.place(x=35, y=470, width=105, height=70)
                        label9 = Label(panel1(), text='GROUND', font=mainfontbold, bg=dynamicBackground(),
                                       fg=dynamicForeground())
                        label9.place(x=10, y=570, width=150, height=15)

                        img10 = makeIcon(file='mainicons/interface/radialindicator.png', height=150, width=150,
                                         mode='manual', color='#313131')
                        self.element10 = Label(panel1(), image=img10, bg=dynamicBackground())
                        self.element10.image = img10
                        self.element10.place(x=190, y=430)
                        self.indicator10 = Label(panel1(), text='ready', font=titlefontbig, bg=dynamicBackground(),
                                                 fg=dynamicForeground())
                        self.indicator10.place(x=215, y=470, width=105, height=70)
                        label10 = Label(panel1(), text='ISOLATE', font=mainfontbold, bg=dynamicBackground(),
                                        fg=dynamicForeground())
                        label10.place(x=190, y=570, width=150, height=15)

                        img11 = makeIcon(file='mainicons/interface/radialindicator.png', height=150, width=150,
                                         mode='manual', color='#313131')
                        self.element11 = Label(panel1(), image=img11, bg=dynamicBackground())
                        self.element11.image = img11
                        self.element11.place(x=370, y=430)
                        self.indicator11 = Label(panel1(), text='ready', font=titlefontbig, bg=dynamicBackground(),
                                                 fg=dynamicForeground())
                        self.indicator11.place(x=395, y=470, width=105, height=70)
                        label11 = Label(panel1(), text='PROGRAM', font=mainfontbold, bg=dynamicBackground(),
                                        fg=dynamicForeground())
                        label11.place(x=370, y=570, width=150, height=15)

                        img12 = makeIcon(file='mainicons/interface/radialindicator.png', height=150, width=150,
                                         mode='manual', color='#313131')
                        self.element12 = Label(panel1(), image=img12, bg=dynamicBackground())
                        self.element12.image = img12
                        self.element12.place(x=550, y=430)
                        self.indicator12 = Label(panel1(), text='ready', font=titlefontbig, bg=dynamicBackground(),
                                                 fg=dynamicForeground())
                        self.indicator12.place(x=575, y=470, width=105, height=70)
                        label12 = Label(panel1(), text='FUNCTION', font=mainfontbold, bg=dynamicBackground(),
                                        fg=dynamicForeground())
                        label12.place(x=550, y=570, width=150, height=15)

                        self.pbar = Frame(panel1(), bg='#939393')
                        self.pbar.place(x=10, y=630, width=730, height=20)

                        self.pbarfilled = Frame(self.pbar, bg=getAccentColor())
                        self.pbarfilled.place(x=0, y=0, relwidth=0, relheight=1)

                        self.pbarprog = Label(panel1(), text='0%', font=titlefontbig, bg=dynamicBackground(),
                                              fg=dynamicForeground())
                        self.pbarprog.place(x=10, y=660)

                        element13 = ColorButton(panel1(), text='Cancel', command=stopdemotest)
                        element13.place(x=530, y=680)

                        element14 = ColorButton(panel1(), text='Start', command=starttest)
                        element14.place(x=640, y=680)

                    class panel2():
                        panel2 = UtilityPanel(parent, bg='red')
                        menu.addElement(title=sm2string2, panelload=panel2,
                                                   icon='mainicons/viapaq.png')  # ETO testing

            class labelPrintingSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring3,
                                                  icon='mainicons/back.png')  # Label printing

                    menu.pack()

                    class panel1():
                        mainwindoww = 1200
                        mainwindowh = 600
                        mainwindowws = mainwindow.winfo_screenwidth()
                        mainwindowhs = mainwindow.winfo_screenheight()
                        x = (mainwindowws / 2) - (mainwindoww / 2)
                        y = (mainwindowhs / 2) - (mainwindowh / 2)
                        mainwindow.geometry('%dx%d+%d+%d' % (mainwindoww, mainwindowh, x, y))

                        panel1 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm3string1, panelload=panel1,
                                                   icon='mainicons/luminary.png')  # Luminary Labels

                        element0 = Label(panel1(), text=sm3string1, font=titlebold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element0.place(x=10, y=10)
                        element1 = Label(panel1(), text='Manual mode', font=mainfontbold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element1.place(x=10, y=70)
                        element2 = Label(panel1(), text="Fill all the fields to print a custom luminary label.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=100)

                        element3 = TextEntry(panel1(), placeholder='Luminary code')
                        element3.place(x=10, y=150, width=540)
                        # element4 = TextEntry(panel1(),placeholder='Date')
                        # element4.place(x=170,y=150)

                        element4 = TextEntry(panel1(), placeholder='Led number')
                        element4.place(x=10, y=200, width=100)
                        element5 = TextEntry(panel1(), placeholder='Sys. Power')
                        element5.place(x=120, y=200, width=100)
                        element6 = TextEntry(panel1(), placeholder='Led flux')
                        element6.place(x=230, y=200, width=100)
                        element7 = TextEntry(panel1(), placeholder='Led color')
                        element7.place(x=340, y=200, width=100)
                        element8 = TextEntry(panel1(), placeholder='Optic')
                        element8.place(x=450, y=200, width=100)

                        element9 = TextEntry(panel1(), placeholder='Voltage')
                        element9.place(x=10, y=240, width=173)
                        element10 = TextEntry(panel1(), placeholder='Frequency')
                        element10.place(x=193, y=240, width=174)
                        element11 = TextEntry(panel1(), placeholder='Power factor')
                        element11.place(x=377, y=240, width=173)

                        element12 = TextEntry(panel1(), placeholder='Temperature')
                        element12.place(x=10, y=280, width=540)

                        element13 = TextEntry(panel1(), placeholder='Program name')
                        element13.place(x=10, y=320, width=540)

                        element14 = TextEntry(panel1(), placeholder='Class')
                        element14.place(x=170, y=500)
                        element15 = TextEntry(panel1(), placeholder='IP')
                        element15.place(x=330, y=500)

                        element16 = CheckBox(panel1(), placeholder='CE')
                        element16.place(x=580, y=150)
                        element17 = CheckBox(panel1(), placeholder='WEE')
                        element17.place(x=650, y=150)
                        element18 = CheckBox(panel1(), placeholder='Broken glass')
                        element18.place(x=580, y=200)

                        element19vars = ['Class I', 'Class II']
                        element19 = ComboBox(panel1(), variables=element19vars, index=0)
                        element19.place(x=580, y=280)

                        element20vars = ['IP54', 'IP55', 'IP56', 'IP57', 'IP58', 'IP59', 'IP60', 'IP61', 'IP62', 'IP63',
                                         'IP64', 'IP65', 'IP66', 'IP67', 'IP68']
                        element20 = ComboBox(panel1(), variables=element20vars, index=12)
                        element20.place(x=580, y=320)

                    panel2 = UtilityPanel(parent, bg='red')
                    menu.addElement(title=sm3string2, panelload=panel2,
                                               icon='mainicons/cardboardbox.png')  # Packaging labels

                    panel3 = UtilityPanel(parent, bg='green')
                    menu.addElement(title=sm3string3, panelload=panel3,
                                               icon='mainicons/globaltronic.png')  # Globaltronic labels

                    panel4 = UtilityPanel(parent, bg='yellow')
                    menu.addElement(title=sm3string4, panelload=panel4,
                                               icon='mainicons/label.png')  # Generic labels

            class individualTestingSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring4,
                                                  icon='mainicons/back.png')  # Single testing

                    menu.pack()

                    panel1 = UtilityPanel(parent, bg='blue')
                    menu.addElement(title=sm4string1, panelload=panel1,
                                               icon='mainicons/dali.png')  # DALI testing

                    label1 = Label(panel1(), text='Hello')
                    label1.place(x=0)

                    panel2 = UtilityPanel(parent, bg='red')
                    menu.addElement(title=sm4string2, panelload=panel2,
                                               icon='mainicons/simpleset.png')  # SIMPLESET testing

                    panel3 = UtilityPanel(parent, bg='green')
                    menu.addElement(title=sm4string3, panelload=panel3,
                                               icon='mainicons/viapaq.png')  # VIAPAQ testing

            class driversSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring5,
                                                  icon='mainicons/back.png')  # Drivers

                    menu.pack()

                    panel1 = UtilityPanel(parent, bg='blue')
                    menu.addElement(title=sm5string1, panelload=panel1,
                                               icon='mainicons/dali.png')  # Philips manual program generation

                    label1 = Label(panel1(), text='Hello')
                    label1.place(x=0)

                    panel2 = UtilityPanel(parent, bg='red')
                    menu.addElement(title=sm5string2, panelload=panel2,
                                               icon='mainicons/viapaq.png')  # VIAPAQ manual program generation

                    panel3 = UtilityPanel(parent, bg='green')
                    menu.addElement(title=sm5string3, panelload=panel3,
                                               icon='mainicons/luminaryoptions.png')  # Name-based program generation

            class productionSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring6,
                                                  icon='mainicons/back.png')  # Production

                    menu.pack()

                    panel1 = UtilityPanel(parent, bg='blue')
                    menu.addElement(title=sm6string1, panelload=panel1,
                                               icon='mainicons/day.png')  # Diary results

                    label1 = Label(panel1(), text='Hello')
                    label1.place(x=0)

                    panel2 = UtilityPanel(parent, bg='red')
                    menu.addElement(title=sm6string2, panelload=panel2,
                                               icon='mainicons/week.png')  # Weekly results

                    panel3 = UtilityPanel(parent, bg='green')
                    menu.addElement(title=sm6string3, panelload=panel3,
                                               icon='mainicons/month.png')  # Monthly results

                    panel4 = UtilityPanel(parent, bg='yellow')
                    menu.addElement(title=sm6string4, panelload=panel4,
                                               icon='mainicons/year.png')  # Annual results

                    panel5 = UtilityPanel(parent, bg='grey')
                    menu.addElement(title=sm6string5, panelload=panel5,
                                               icon='mainicons/customsearchcalendar.png')  # Custom search

            class luminarySubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring7,
                                                  icon='mainicons/back.png')  # Luminary information

                    menu.pack()

                    panel1 = UtilityPanel(parent, bg='blue')
                    menu.addElement(title=sm7string1, panelload=panel1,
                                               icon='mainicons/luminaryoptions.png')  # Check luminary data

                    label1 = Label(panel1(), text='Hello')
                    label1.place(x=0)

                    panel2 = UtilityPanel(parent, bg='red')
                    menu.addElement(title=sm7string2, panelload=panel2,
                                               icon='mainicons/editproperty.png')  # Modify luminary open options

            class settingsSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring8,
                                                  icon='mainicons/back.png')  # System preferences

                    menu.pack()

                    class panel1():
                        def setip(self):
                            myprefs.serverip = str(self.get())
                        panel1 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm8string2, panelload=panel1,
                                                   icon='mainicons/database.png')  # Database

                        element0 = Label(panel1(), text=sm8string2, font=titlebold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element0.place(x=10,y=10)

                        element1 = Label(panel1(), text='Conexión', font=mainfontbold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element1.place(x=10, y=70)
                        element2 = Label(panel1(),
                                         text="En este panel podrás modificar la dirección IP del servidor en el cual se realizan todas las acciones del programa.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=100)
                        element3 = Label(panel1(), text='Dirección IP:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element3.place(x=10, y=160)
                        self.element4 = TextEntry(panel1(), text=myprefs.serverip,action=setip)
                        self.element4.place(x=13, y=190, width=250)

                    class panel2():#Serial Port
                        def settestmachineserialport(self):
                            myprefs.testmachineserialport = str(self.get())
                        def settestmachineserialbauds(self):
                            myprefs.testmachineserialbauds = str(self.get())
                        def settestmachineserialparity(self):
                            myprefs.testmachineserialparity = str(self.get())
                        def settestmachineserialbytesize(self):
                            myprefs.testmachineserialbytesize = str(self.get())
                        def settestmachineserialstopbits(self):
                            myprefs.testmachineserialstopbits = str(self.get())
                        def setluxometerserialport(self):
                            myprefs.luxometerserialbauds = str(self.get())
                        def setluxometerserialbauds(self):
                            myprefs.luxometerserialbauds = str(self.get())
                        def setluxometerserialparity(self):
                            myprefs.luxometerserialparity = str(self.get())
                        def setluxometerserialbytesize (self):
                            myprefs.luxometerserialbytesize = str(self.get())
                        def setluxometerserialstopbits(self):
                            myprefs.luxometerserialstopbits = str(self.get())

                        panel2 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm8string1, panelload=panel2,
                                                   icon='mainicons/serialport.png')  # Serial port

                        element0 = Label(panel2(), text=sm8string1, font=titlebold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element0.place(x=10,y=10)
                        element1 = Label(panel2(), text='Schleich GLP2-e Test Machine', font=mainfontbold,
                                         bg=dynamicBackground(), fg=dynamicForeground())
                        element1.place(x=10, y=70)
                        element2 = Label(panel2(),
                                         text='Recommended settings for the serial port connection if the Schleich GLP2-e Test Machine are:\n9600 bauds, 8,N,1',
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=100)
                        element3 = Label(panel2(), text='Serial port', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element3.place(x=10, y=170)
                        serialportlist = ['COM1','COM2','COM3','COM4','COM5','COM6','COM7']
                        element4 = ComboBox(panel2(), variables=serialportlist, index=0,action=settestmachineserialport)
                        element4.place(x=13, y=210)
                        element5 = Label(panel2(), text='Bauds', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element5.place(x=200, y=170)
                        element6 = TextEntry(panel2(), text='9600',action=settestmachineserialbauds)
                        element6.place(x=203, y=210)

                        element13 = Label(panel2(), text='Bytesize', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element13.place(x=10, y=260)
                        bytesizelist = ['FIVEBITS','SIXBITS','SEVENBITS','EIGHTBITS']
                        element14 = ComboBox(panel2(), variables=bytesizelist,index=3)
                        element14.place(x=13, y=300)
                        element15 = Label(panel2(), text='Parity', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element15.place(x=200, y=260)
                        paritylist = ['PARITY_NONE','PARITY_EVEN','PARITY_ODD','PARITY_MARK','PARITY_SPACE']
                        element16 = ComboBox(panel2(), variables=paritylist,index=0)
                        element16.place(x=203, y=300)
                        element15 = Label(panel2(), text='Stopbits', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element15.place(x=400, y=260)
                        stopbitslist = ['STOPBITS_ONE','STOPBITS_ONE_POINT_FIVE','STOPBITS_TWO']
                        element16 = ComboBox(panel2(), variables=stopbitslist,index=0)
                        element16.place(x=403, y=300)

                        element7 = Label(panel2(), text='Konica Minolta Luxometer', font=mainfontbold,
                                         bg=dynamicBackground(), fg=dynamicForeground())
                        element7.place(x=10, y=360)
                        element8 = Label(panel2(),
                                         text='Recommended settings for the serial port connection if the Minolta luxometer are:\n9600 bauds, 8,PARITY_EVEN,1',
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element8.place(x=10, y=390)
                        element9 = Label(panel2(), text='Serial port', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element9.place(x=10, y=460)
                        element10 = ComboBox(panel2(), variables=serialportlist, index=0)
                        element10.place(x=13, y=500)
                        element11 = Label(panel2(), text='Bauds', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element11.place(x=200, y=460)
                        element12 = TextEntry(panel2(), text='9600')
                        element12.place(x=203, y=500)
                        element13 = Label(panel2(), text='Bytesize', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element13.place(x=10, y=550)
                        element14 = ComboBox(panel2(), variables=bytesizelist,index=0)
                        element14.place(x=13, y=590)
                        element15 = Label(panel2(), text='Parity', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element15.place(x=200, y=550)
                        element16 = ComboBox(panel2(), variables=paritylist,index=0)
                        element16.place(x=203, y=590)
                        element15 = Label(panel2(), text='Stopbits', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element15.place(x=400, y=550)
                        element16 = ComboBox(panel2(), variables=stopbitslist,index=0)
                        element16.place(x=403, y=590)

                        elementx = Label(panel2(),bg=dynamicBackground())
                        elementx.place(x=0,y=650,height=100)

                    class panel3():
                        def setlanguageselected(self):
                            myprefs.languageselected = str(self.get())
                        panel3 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm8string3, panelload=panel3,
                                                   icon='mainicons/language.png')  # Language

                        element0 = Label(panel3(), text=sm8string3, font=titlebold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element0.place(x=10, y=10)
                        element1 = Label(panel3(), text='Idioma', font=mainfontbold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element1.place(x=10, y=70)
                        element2 = Label(panel3(),
                                         text="Desde aquí podrás modificar el idioma del programa.\nPara que los cambios se apliquen, por favor reinicie el programa.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=100)
                        element3 = RadioButton(panel3(), text='Castellano', image='mainicons/interface/spainflag.png',variable=myprefs.languageselected,value='ESP')
                        element3.place(x=10, y=180)
                        element4 = RadioButton(panel3(), text='English', image='mainicons/interface/ukflag.png',variable=myprefs.languageselected,value='ENG')
                        element4.place(x=10, y=240)

                    class panel4():
                        def setcameraenabled(self):
                            myprefs.cameraenabled = str(self.get())
                        panel4 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm8string4, panelload=panel4,
                                                   icon='mainicons/camera.png')  # Camera
                        element1 = Label(panel4(), text='Cámara', font=mainfontbold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element1.place(x=10, y=10)
                        element2 = Label(panel4(),
                                         text="Modifica las opciones del programa relacionadas con la cámara.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=40)
                        element3 = Label(panel4(), text='Nombre:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element3.place(x=10, y=100)
                        element4 = TextEntry(panel4(), text=myprefs.username)
                        element4.place(x=13, y=130, width=250)

                    class panel5():
                        def setluminaryprinter(self):
                            myprefs.luminaryprinter = str(self.get())
                        def setluminaryenabled(self):
                            myprefs.luminaryenabled = str(self.get())
                        def setluminaryprintingmode(self):
                            myprefs.luminaryprintingmode = str(self.get())
                        def setpackagingprinter(self):
                            myprefs.packagingprinter = str(self.get())
                        def setpackagingenabled(self):
                            myprefs.packagingenabled = str(self.get())
                        def setuserguideprinter(self):
                            myprefs.userguideprinter = str(self.get())
                        def setuserguideenabled(self):
                            myprefs.userguideenabled = str(self.get())
                        panel5 = UtilityPanel(parent, bg=dynamicBackground())
                        menu.addElement(title=sm8string5, panelload=panel5,
                                                   icon='mainicons/printers.png')  # Printers

                        element0 = Label(panel5(), text=sm8string5, font=titlebold, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element0.place(x=10, y=10)
                        element1 = Label(panel5(), text='Luminary label printer', font=mainfontbold,
                                         bg=dynamicBackground(), fg=dynamicForeground())
                        element1.place(x=10, y=70)
                        element2 = Label(panel5(),
                                         text="Set up the printer that print the luminary labels.\nYou need to set the printer, the number of labels and if it's enabled or not.\nPrinting mode option defines the number of labels that it will print if the result is OK.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element2.place(x=10, y=100)
                        element3 = Label(panel5(), text='Select printer:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element3.place(x=10, y=190)
                        printers = []
                        printerlist = win32print.EnumPrinters(3)
                        for i in range(len(printerlist)):
                            printers.append(printerlist[i][2])
                        luminaryindex = 0
                        for i in range(len(printers)):
                            if printers[i] == myprefs.luminaryprinter:
                                luminaryindex = i
                        element4 = ComboBox(panel5(), variables=printers, index=luminaryindex,action=setluminaryprinter)
                        element4.place(x=13, y=230, width=400)

                        element5 = Switch(panel5(), placeholder='Enable',action=setluminaryenabled)
                        element5.place(x=13, y=270)
                        element6 = Label(panel5(), text='Printing mode:', font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element6.place(x=10, y=310)
                        element7vars = ['Automatic', 'One label', 'Two labels']
                        element7 = ComboBox(panel5(), variables=element7vars, index=0,action=setluminaryprintingmode)
                        element7.place(x=13, y=340, width=400)

                        element8 = Label(panel5(), text='Packaging label printer', font=mainfontbold,
                                         bg=dynamicBackground(), fg=dynamicForeground())
                        element8.place(x=10, y=400)
                        element9 = Label(panel5(),
                                         text="Set up the printer that print the packaging labels.\nYou need to set the printer, the number of labels and if it's enabled or not.",
                                         anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                         fg=dynamicForeground())
                        element9.place(x=10, y=430)
                        element10 = Label(panel5(), text='Select printer:', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element10.place(x=10, y=490)
                        packagingindex = 0
                        for i in range(len(printers)):
                            if printers[i] == myprefs.packagingprinter:
                                packagingindex = i
                        element11 = ComboBox(panel5(), variables=printers, index=packagingindex,action=setpackagingprinter)
                        element11.place(x=13, y=530, width=400)

                        element12 = Switch(panel5(), placeholder='Enable',action=setpackagingenabled)
                        element12.place(x=13, y=570)

                        element13 = Label(panel5(), text='User guide printer', font=mainfontbold,
                                          bg=dynamicBackground(), fg=dynamicForeground())
                        element13.place(x=10, y=630)
                        element14 = Label(panel5(),
                                          text="Set up the printer that print the user guides.\nYou need to set the printer, the number of labels and if it's enabled or not.",
                                          anchor=W, justify=LEFT, wraplength=550, font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element14.place(x=10, y=660)
                        element15 = Label(panel5(), text='Select printer:', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element15.place(x=10, y=720)
                        userguideindex = 0
                        for i in range(len(printers)):
                            if printers[i] == myprefs.userguideprinter:
                                userguideindex = i
                        element16 = ComboBox(panel5(), variables=printers, index=userguideindex,action=setuserguideprinter)
                        element16.place(x=13, y=750, width=400)

                        element17 = Switch(panel5(), placeholder='Enable',action=setuserguideenabled)
                        element17.place(x=13, y=790)
                        element15 = Label(panel5(), text=' ', font=mainfont, bg=dynamicBackground(),
                                          fg=dynamicForeground())
                        element15.place(x=10, y=860, height=200, width=100)

            class miscSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring9,
                                                  icon='mainicons/back.png')  # Other actions

                    menu.pack()

                    panel1 = UtilityPanel(parent, bg='blue')
                    menu.addElement(title=sm9string1, panelload=panel1,
                                               icon='mainicons/camera2.png')  # Check camera

                    label1 = Label(panel1(), text='Hello')
                    label1.place(x=0)

                    panel2 = UtilityPanel(parent, bg='red')
                    menu.addElement(title=sm9string2, panelload=panel2,
                                               icon='mainicons/luxometer.png')  # Check luxometer

                    panel3 = UtilityPanel(parent, bg='green')
                    menu.addElement(title=sm9string3, panelload=panel3,
                                               icon='mainicons/testmachine.png')  # Test machine actions

                    panel4 = UtilityPanel(parent, bg='yellow')
                    menu.addElement(title=sm9string4, panelload=panel4,
                                               icon='mainicons/electricalthreshold.png')  # Test w/o machine (admin. required)

                    panel5 = UtilityPanel(parent, bg='grey')
                    menu.addElement(title=sm9string5, panelload=panel5,
                                               icon='mainicons/cancel.png')  # Incidences

            class helpSubMenu:
                def __init__(self, parent):
                    menu = LeftSideBar(parent, backtext=sysmesstring1, title=mmstring10,
                                                  icon='mainicons/back.png')  # Help

                    menu.pack()

                    panel1 = UtilityPanel(parent, bg='blue')
                    menu.addElement(title=sm10string1, panelload=panel1, icon='mainicons/help.png')  # FAQ

                    label1 = Label(panel1(), text='Hello')
                    label1.place(x=0)

                    panel2 = UtilityPanel(parent, bg='red')
                    menu.addElement(title=sm10string2, panelload=panel2,
                                               icon='mainicons/results.png')  # User guide

            menu.addElement(title=mmstring1, description=mmdescstring1, icon='mainicons/user.png',
                            command=userSubMenu)  # 'Manage the user information and options related...'
            menu.addElement(title=mmstring2, description=mmdescstring2, icon='mainicons/testglobal.png',
                            command=orderTestingSubMenu)  # Check and validation of luminaries correct functioning.
            menu.addElement(title=mmstring3, description=mmdescstring3, icon='mainicons/label.png',
                            command=labelPrintingSubMenu)  # Design and print manually labels, box labels and others.
            menu.addElement(title=mmstring4, description=mmdescstring4, icon='mainicons/testind.png',
                            command=individualTestingSubMenu)  # Check and validate luminaries individually.
            menu.addElement(title=mmstring5, description=mmdescstring5, icon='mainicons/philipsdriver.png',
                            command=driversSubMenu)  # Manual generation of programming files for Philips, Viapaq, ELT...
            menu.addElement(title=mmstring6, description=mmdescstring6, icon='mainicons/results.png',
                            command=productionSubMenu)  # Check test results and general production results.
            menu.addElement(title=mmstring7, description=mmdescstring7, icon='mainicons/luminary.png',
                            command=luminarySubMenu)  # Modify luminary data or check if all data and description is correct.
            menu.addElement(title=mmstring8, description=mmdescstring8, icon='mainicons/settings.png',
                            command=settingsSubMenu)  # Edit the system settings to make everything works correctly.
            menu.addElement(title=mmstring9, description=mmdescstring9, icon='mainicons/misc.png',
                            command=miscSubMenu)  # Miscellaneous.
            menu.addElement(title=mmstring10, description=mmdescstring10, icon='mainicons/help.png',
                            command=helpSubMenu)  # Frequently asked questions and user guide.

    boosMainMenu(mainwindow)

    mainwindow.protocol("WM_DELETE_WINDOW", on_closing)
    mainwindow.mainloop()


initmainwindow()
