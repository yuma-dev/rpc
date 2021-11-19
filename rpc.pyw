import logging,sys,ctypes,pyuac,configparser

config = configparser.ConfigParser()
config.read("data/config.ini")
config = config['rpc']

if config['AdminMode'] == 'no' or pyuac.isUserAdmin() == True:
    

    class LogFile(object):

        def __init__(self, name=None):
            self.logger = logging.getLogger(name)

        def write(self, msg, level=logging.INFO):
            self.logger.log(level, msg)

        def flush(self):
            for handler in self.logger.handlers:
                handler.flush()
    sys.stdout = LogFile('stdout')
    sys.stderr = LogFile('stderr')
    logging.basicConfig(level=logging.DEBUG, filename='logs/logging.log', format = '%(asctime)s | %(levelname)s  -  %(message)s')
    try:
        #imports
        import wx.adv,wx,atexit,psutil,threading,time,win32gui,win32process,os,traceback,json,easygui , tkinter as tk,pypresence
        from modules import playtime,readable,yasuo,officialAddons,customAddons #custom module for client data
        from datetime import datetime #get the current time for logging errors
        from pynput import keyboard #check for hotkey
        from PySide2 import QtWidgets, QtGui
        from SwSpotify import spotify #get playing track info
        from win10toast import ToastNotifier #push desktop notifications
        from ctypes import windll
        from youtube_search import YoutubeSearch
        from tkinter.scrolledtext import *

        #DEFAULTING
        icon_path = "sprites/icon.ico"
        toast = ToastNotifier()
        global globaldetails,globalstate,globallarge_image,globallarge_text,globalsmall_image,globalsmall_text,loops,looptime
        hidden = False
        globaldetails = None
        globalstate = None
        globallarge_image = None
        globallarge_text = None
        hiddenText = 'Enable AFK'
        globalsmall_image = None
        globalsmall_text = None
        loops = 0
        start_time = time.time()
        looptime = int(config['LoopTime'])


        def atStart():
            with open('logs/status.txt', 'w') as f:
                f.write('on')

        def atExit(): #function gets called on exit unless the python process gets killed
            with open('logs/status.txt', 'w') as f:
                f.write('off')

        def getStatus():
            with open('logs/status.txt', 'r') as f:
                return f.read()



        def logError(e):
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.critical(e) #print error message(for debug)
            logging.critical(f'DEBUG : {exc_type} {fname} in line {exc_tb.tb_lineno}') #print



        def openLogs():
            window = tk.Tk()
            window.wm_title("Logs")
            TextBox = ScrolledText(window, height='50', width='70', wrap=tk.WORD,font=("Consolas", 10))

            OPTIONS = [
                "all",
                "INFO",
                "DEBUG",
                "WARNING",
                "ERROR",
                "CRITICAL"
            ]
            variable = tk.StringVar(window)
            variable.set(OPTIONS[0]) # default value

            def updater():
                update()
                window.after(2000, updater)

            def update():
                with open(os.getcwd()+'\\logs\\logging.log', 'r') as logs:
                    TextBox.delete('1.0', tk.END)
                    if variable.get() == "all":
                        TextBox.insert(tk.END, logs.read())
                    else:
                        if variable.get() == "INFO":
                            for line in logs.readlines():
                                if 'INFO' in line:
                                    TextBox.insert(tk.END, line)
                                if 'DEBUG' in line:
                                    TextBox.insert(tk.END, line)
                                if 'WARNING' in line:
                                    TextBox.insert(tk.END, line)
                                if 'CRITICAL' in line:
                                    TextBox.insert(tk.END, line)
                                if 'ERROR' in line:
                                    TextBox.insert(tk.END, line)
                        if variable.get() == "DEBUG":
                            for line in logs.readlines():
                                if 'DEBUG' in line:
                                    TextBox.insert(tk.END, line)
                                if 'WARNING' in line:
                                    TextBox.insert(tk.END, line)
                                if 'CRITICAL' in line:
                                    TextBox.insert(tk.END, line)
                                if 'ERROR' in line:
                                    TextBox.insert(tk.END, line)
                        if variable.get() == "WARNING":
                            for line in logs.readlines():
                                if 'WARNING' in line:
                                    TextBox.insert(tk.END, line)
                                if 'CRITICAL' in line:
                                    TextBox.insert(tk.END, line)
                                if 'ERROR' in line:
                                    TextBox.insert(tk.END, line)
                        if variable.get() == "ERROR":
                            for line in logs.readlines():
                                if 'CRITICAL' in line:
                                    TextBox.insert(tk.END, line)
                                if 'ERROR' in line:
                                    TextBox.insert(tk.END, line)
                        if variable.get() == "CRITICAL":
                            for line in logs.readlines():
                                if 'CRITICAL' in line:
                                    TextBox.insert(tk.END, line)
                    TextBox.yview(tk.END)
                

            def clearLogs():
                open(os.getcwd()+'\\logs\\logging.log', 'w').close()
                update()


            window.after(2000, updater)

            update()


            def deleter():
                TextBox.delete('1.0', tk.END)


            window.resizable(height = None, width = None)
            clearButton = tk.Button(window, text="Clear", command=clearLogs)
            deleteButton = tk.Button(window, text="Delete", command=deleter)
            filterSelection = tk.OptionMenu(window,variable, *OPTIONS)
            TextBox.pack(fill=tk.BOTH,expand=tk.YES)
            filterSelection.pack()
            clearButton.pack()
            deleteButton.pack()
            tk.mainloop()

        
        class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
            """
            CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
            """
            def __init__(self, icon, parent=None):
                QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
                self.setToolTip(f'Custom Discord Rich Presence')
                menu = QtWidgets.QMenu(parent)
                open_app = menu.addAction("Restart")
                open_app.triggered.connect(self.on_restart)
                open_app.setIcon(QtGui.QIcon("sprites/restart.png"))

                open_app = menu.addAction("Open Logs")
                open_app.triggered.connect(self.open_logs)
                open_app.setIcon(QtGui.QIcon("sprites/logs.png"))

                open_cal = menu.addAction("Toggle AFK")
                open_cal.triggered.connect(self.toggle_afk)
                open_cal.setIcon(QtGui.QIcon("sprites/afk.png"))

                exit_ = menu.addAction("Exit")
                exit_.triggered.connect(self.on_exit)
                exit_.setIcon(QtGui.QIcon("sprites/exit.png"))

                menu.addSeparator()
                self.setContextMenu(menu)
                self.activated.connect(self.onTrayIconActivated)

            def onTrayIconActivated(self, reason):
                """
                This function will trigger function on click or double click
                :param reason:
                :return:
                """
                print('Activated')
                #if reason == self.DoubleClick:
                #    self.open_notepad()
                # if reason == self.Trigger:
                #     self.open_notepad()

            def toggle_afk(self):
                toggleHidden()

            def on_restart(self):
                logging.warn('Restarting...')
                time.sleep(3)
                os.execv(sys.executable, ['pyw'] + sys.argv)

            def open_logs(self):
                openLogs()

            def on_exit(self):
                psutil.Process(os.getpid()).terminate()


        def startTray():
            app = QtWidgets.QApplication(sys.argv)
            w = QtWidgets.QWidget()
            tray_icon = SystemTrayIcon(QtGui.QIcon("sprites/icon.png"), w)
            tray_icon.show()
            sys.exit(app.exec_())

        def toggleHidden():
            global hidden
            if config['AFKToggle'] == 'yes':
                if hidden is True: #set hidden variable to False if it's already True and give Windows notification
                    toast.show_toast("rpc.pyw","no longer afk!",duration=3,icon_path=icon_path,threaded=True)
                    hidden = False
                    hiddenText = 'Disable AFK'
                    logging.info("Disabled AFK mode")
                elif hidden is False: #set hidden variable to True if it's already False and give Windows notification
                    toast.show_toast("rpc.pyw","now afk!",duration=3,icon_path=icon_path,threaded=True)
                    hidden = True
                    hiddenText = 'Enable AFK'
                    logging.info("Enabled AFK mode")
        

        def reset():
            logging.warning("Resetting...")
            os.execv(sys.executable, ['pyw'] + sys.argv)

        def resettimer():
            time.sleep(900)
            if hidden is False:
                reset()


        #thread hotkeylistener and timer
        if config['ResetTimer'] == 'yes':
            rTimer = threading.Thread(target=resettimer)
            rTimer.start()
        if config['SystemTray'] == 'yes':
            sTray = threading.Thread(target=startTray)
            sTray.start()
        logging.info('Done!')

            

        while True:
            try:
                
                #connect to application via id on pipe 0
                client_id = str(config['ClientID']) #set discord application id
                RPC = pypresence.Presence(client_id) #set the client with id and define what pipe
                RPC.connect() #connect to the client

                while True:  #infinite loop 

                    #default update variable to False
                    update = False

                    #get hardware usage (Disabled)
                    #cpu_per = round(psutil.cpu_percent(),1)
                    if config['Spotify'] == 'yes':
                        try: #will succeed if a song is playing
                            playing = True
                            image = "spotify"
                            statetext = "♫ 𝔩𝔦𝔰𝔱𝔢𝔫𝔦𝔫𝔤 𝔱𝔬 𝔪𝔲𝔰𝔦𝔠 ♫"
                            largetext = "The open program has no set Image"
                            largeimage = "unknown"
                            state =spotify.song()+" ~ "+spotify.artist()

                        except Exception: #will trigger if no song is playing
                            playing = False
                            image = None #"heart"
                            state = None #"Λ 24.02.2020"
                            statetext = None #"𝗖𝗣𝗨: "+str(cpu_per)+"%"
                            largetext = "The open program has no set Image"
                            largeimage = "unknown"

                    #get process id
                    w=win32gui #shortversion
                    dataName = "ERROR"
                    try:
                        
                        pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow()) #get ForegroundWindow ID
                        openwindow = psutil.Process(pid[-1]).name() #get the window name through the ID
                        openwindow = openwindow[:-4] #remove .exe
                        openwindowtitle = w.GetWindowText(w.GetForegroundWindow())
                        showplaying = True #default to True
                        dataName = openwindow
                    except Exception as e:
                        logError(e)
                        openwindow = "ERROR"
                        openwindowtitle = "ERROR"
                        showplaying = True #default to True
                        dataName = openwindow

                    #if its not hidden
                    if not hidden:
                        if config['CustomModules'] == 'yes':
                            openwindow,dataName,largeimage,largetext,state,image,showplaying = customAddons.getData(openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying)
                        if config['OfficialModules'] == 'yes': 
                            openwindow,dataName,largeimage,largetext,state,image,showplaying = officialAddons.getData(openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying)
        



                    elif hidden: #if the hidden/afk mode is true

                        showplaying = False
                        openwindow = '💤 ⓐⓕⓚ 💤'
                        largeimage = 'afk'
                        dataName = "afk"
                        largetext = 'Not available on PC'

                    #limit if over 128 chars
                    if largetext:
                        largetext = largetext[:125] + (largetext[125:] and '...')
                    
                    #if it's a not defined window, display it this way:
                    if showplaying:
                        if config['SpecialUndefined'] == 'yes':
                            openwindow = '《'+openwindow+'》'

                    

                    #if anything changed, set update to True
                    needs_update = [globaldetails != openwindow, globalstate != statetext, globallarge_image != largeimage, globallarge_text != largetext, globalsmall_image != image, globalsmall_text != state]
                    if any(needs_update):
                        update = True

                    if config['AlwaysUpdate'] == 'yes':
                        update = True


                    if dataName:
                        if config['LogTime'] == 'yes':
                            print(dataName+' '+str(looptime))
                            try:
                                playtime.write(str(dataName), looptime)
                            except:
                                pass
                            
                    
                    #resets timer every time a new application is showed    
                    #if globaldetails != openwindow:
                        #start_time = time.time()

                    #if update is True, update the RPC
                    if config['Button'] == 'yes':
                        if config['CustomButton'] == 'yes':
                            buttons=[{
                                "label": str(config['CustomLabel']), #set button label
                                "url": str(config['CustomUrl']) #set button link
                                }]
                        else:
                            buttons=[{
                                "label": "ʟᴀɴᴛᴇʀɴ.ʟᴏʟ", #set button label
                                "url": "https://Lantern.LoL" #set button link
                                }]
                    else:
                        buttons = None
                    if update:
                        #update connection to rpc server with all detail
                        RPC.update(
                            details=openwindow, #currently open window name
                            state=statetext, #current cpu usage
                            large_image=largeimage, #set large image 
                            large_text=largetext, #set large image text
                            small_image=image, #set small image
                            small_text=state, #set small image text
                            buttons=buttons
                            )

                        #set the last update to check in the next loop
                        globaldetails = openwindow
                        globalstate = statetext
                        globallarge_image = largeimage
                        globallarge_text = largetext
                        globalsmall_image = image
                        globalsmall_text = state

                    #wait 30 seconds then repeat the loop
                    time.sleep(looptime)
                    loops += 1
                    logging.info(f'Looped!')
                    
                    
                        
            #if an error occurs while running the loop (mostly rpc not being able to connect to discord due to discord being closed)
            except Exception as e:
                print(f"'{e}'")
                if str(e) == "Pipe Not Found - Is Discord Running?":
                    logging.critical("Discord is not open yet, trying again in 15 seconds...")
                    time.sleep(15)
                    continue
                else:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    logging.critical(e) #print error message(for debug)
                    logging.critical(f'DEBUG : {exc_type} {fname} in line {exc_tb.tb_lineno}') #print
                    easygui.msgbox(f"DEBUG : {exc_type} {fname} in line {exc_tb.tb_lineno}\n{e}", "RPC Error")
                    exit()
    except Exception as e:
        logging.critical(e)
else:
    pyuac.runAsAdmin()