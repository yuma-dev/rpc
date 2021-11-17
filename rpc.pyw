import logging
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    

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
        import wx.adv #tray
        import wx #tray
        from ctypes import windll
        import atexit
        import psutil #get hardware data
        import threading #run multiple loops
        import time #sleep
        import win32gui #get focussed window
        import win32process #get focussed window
        from modules import * #custom module for client data
        import os #restart script occasionally
        import traceback #get tracebacks for logs
        import json #get json data
        import readable #make things readable
        from datetime import datetime #get the current time for logging errors
        from pynput import keyboard #check for hotkey
        from pypresence import Presence #update local discord rich presence
        from PySide2 import QtWidgets, QtGui
        from SwSpotify import spotify #get playing track info
        from win10toast import ToastNotifier #push desktop notifications
        import tkinter as tk
        from tkinter.scrolledtext import *
        from youtube_search import YoutubeSearch #get youtube search info

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
        looptime = 30

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
                open('logs/logging.log', 'w').close()
                psutil.Process(os.getpid()).terminate()


        def startTray():
            app = QtWidgets.QApplication(sys.argv)
            w = QtWidgets.QWidget()
            tray_icon = SystemTrayIcon(QtGui.QIcon("sprites/icon.png"), w)
            tray_icon.show()
            sys.exit(app.exec_())

        def toggleHidden():
            global hidden
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
        rTimer = threading.Thread(target=resettimer)
        rTimer.start()
        sTray = threading.Thread(target=startTray)
        sTray.start()
        logging.info('Done!')

            

        while True:
            try:
                
                #connect to application via id on pipe 0
                client_id = '828958778866270238' #set discord application id
                RPC = Presence(client_id) #set the client with id and define what pipe
                RPC.connect() #connect to the client

                while True:  #infinite loop 

                    #default update variable to False
                    update = False

                    #get hardware usage (Disabled)
                    #cpu_per = round(psutil.cpu_percent(),1)

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
                        
                        #if the window is League of Legends, get all data thats needed and use it
                        if openwindow == 'League of Legends':
                            
                            if playing == False:
                                statetext = "hover the icon for stats"
                                image = "lolsearch"

                            #get ingame data
                            me = yasuo.get_currentuser() #set me as my league username
                            friends = ['Sαyuri','Glennie101','Wallecho','Sturmi101','Sayji','Ahrier69','Takrα','LetsGameDanny','Yumα'] #list with friends usernames
                            mode = yasuo.get_currentmode() #get current league gamemode 
                            champion = yasuo.get_clientdata(me,'champion') #get my current champion
                            kda = yasuo.get_clientdata(me,'kda') #get my kda
                            cs = yasuo.get_clientdata(me,'cs') #get my cs
                            visionscore = yasuo.get_clientdata(me,'vision') #get my vision score
                            gametime = yasuo.get_clientdata(me,'time') #get the current gametime

                            #visuals
                            showplaying = False
                            openwindow = '🎮: 𝚃𝚒𝚕𝚝 𝚘𝚏 𝙻𝚎𝚐𝚎𝚗𝚍𝚜'
                            largeimage = 'leagueingame'

                            #set text
                            friendsingame = [] #create a list

                            for friend in friends: #for each friend in the list of friends usernames
                                if yasuo.check_playeringame(friend): #check if the friend is in my game
                                    friendsingame.append(friend) # add the friend to the list 
                                    
                            if me in friendsingame:
                                friendsingame.remove(me)
                            if playing:
                                if me != 'Yumα':
                                    if friendsingame: #if the friendlist isn't empty it will act as a True statement
                                        if len(friendsingame)>1:
                                            friendlist = " and ".join([",".join(friendsingame[:-1]),friendsingame[-1]]) #for each friend in the list, turn it into a string with one comma inbetween and the last one a " and "
                                        else:
                                            friendlist = ','.join(friendsingame)
                                            
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            largetext = f"Playing {mode} as {champion} {kda} and with {cs} cs on {me}'s account with {friendlist}" #set text to text with mode and friends
                                        else: #if the mode is something else than the normal mode
                                            largetext = f"Playing as {champion} {kda} and with {cs} cs on {me}'s account with {friendlist}" #set text to text with friends
                                    else: #if the friendlist is empty it will act as a False statement
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            largetext = f"Playing {mode} as {champion} {kda} and with {cs} cs since on {me}'s account" #set text to text with mode
                                        else: #if the mode is something other than the normal mode
                                            largetext = f"Playing as {champion} {kda} and with {cs} cs since on {me}'s account" #set text to text
                                else:
                                    if friendsingame: #if the friendlist isn't empty it will act as a True statement
                                        if len(friendsingame)>1:
                                            friendlist = " and ".join([",".join(friendsingame[:-1]),friendsingame[-1]]) #for each friend in the list, turn it into a string with one comma inbetween and the last one a " and "
                                        else:
                                            friendlist = ','.join(friendsingame)
                                            
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            largetext = f'Playing {mode} as {champion} {kda} and with {cs} cs with {friendlist}' #set text to text with mode and friends
                                        else: #if the mode is something else than the normal mode
                                            largetext = f'Playing as {champion} {kda} and with {cs} cs with {friendlist}' #set text to text with friends
                                    else: #if the friendlist is empty it will act as a False statement
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            largetext = f"Playing {mode} as {champion} {kda} and with {cs} cs" #set text to text with mode
                                        else: #if the mode is something other than the normal mode
                                            largetext = f"Playing as {champion} {kda} and with {cs} cs" #set text to text

                            else:
                                ptime = readable.time(seconds=playtime.read(dataName), granularity=2, limit='h', language='en')
                                largetext = f'Tracked Time : {ptime} '
                                if me != 'Yumα':
                                    if friendsingame: #if the friendlist isn't empty it will act as a True statement
                                        if len(friendsingame)>1:
                                            friendlist = " and ".join([",".join(friendsingame[:-1]),friendsingame[-1]]) #for each friend in the list, turn it into a string with one comma inbetween and the last one a " and "
                                        else:
                                            friendlist = ','.join(friendsingame)
                                            
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            state = f"Playing {mode} as {champion} {kda} and with {cs} cs on {me}'s account with {friendlist}" #set text to text with mode and friends
                                        else: #if the mode is something else than the normal mode
                                            state = f"Playing as {champion} {kda} and with {cs} cs on {me}'s account with {friendlist}" #set text to text with friends
                                    else: #if the friendlist is empty it will act as a False statement
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            state = f"Playing {mode} as {champion} {kda} and with {cs} cs since on {me}'s account" #set text to text with mode
                                        else: #if the mode is something other than the normal mode
                                            state = f"Playing as {champion} {kda} and with {cs} cs since on {me}'s account" #set text to text
                                else:
                                    if friendsingame: #if the friendlist isn't empty it will act as a True statement
                                        if len(friendsingame)>1:
                                            friendlist = " and ".join([",".join(friendsingame[:-1]),friendsingame[-1]]) #for each friend in the list, turn it into a string with one comma inbetween and the last one a " and "
                                        else:
                                            friendlist = ','.join(friendsingame)
                                            
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            state = f'Playing {mode} as {champion} {kda} and with {cs} cs with {friendlist}' #set text to text with mode and friends
                                        else: #if the mode is something else than the normal mode
                                            state = f'Playing as {champion} {kda} and with {cs} cs with {friendlist}' #set text to text with friends
                                    else: #if the friendlist is empty it will act as a False statement
                                        if mode != 'CLASSIC': #if the mode isn't the normal mode
                                            state = f"Playing {mode} as {champion} {kda} and with {cs} cs" #set text to text with mode
                                        else: #if the mode is something other than the normal mode
                                            state = f"Playing as {champion} {kda} and with {cs} cs" #set text to text
                                        
                        #all other elif's for checking if a window is a customized one and if it is, take different name,image,and imagetext and say that its a defined window
                        elif openwindow == 'Code':
                            showplaying = False
                            try:
                                openfile = openwindowtitle.replace(' ', '').replace('●', '').split('-')
                                openwindow = f'💿: writing {openfile[0]}'
                            except Exception as e:
                                logError(e)
                                openwindow = 'vsCode'
                            largeimage = 'vscode'
                            largetext = "if str(life.activity) in shitThings :\n os.startfile('LeagueOfLegends.exe')"

                        elif openwindow == 'explorer':
                            showplaying = False
                            openwindow = '📁: Explorer'

                        elif openwindow == 'LeagueClientUx':
                            dataName = "League of Legends"
                            showplaying = False
                            openwindow = '🎮: League Lobby'
                            largeimage = 'leaguelobby'
                            largetext = 'Looking to play a game..'

                        elif openwindow == 'RiotClientUx':
                            dataName = "League of Legends"
                            showplaying = False
                            openwindow = '🎮: logging in...'
                            largeimage = 'riotclient'
                            largetext = 'User: YumaIsBack\nPassword: deggubkcitS'

                        elif openwindow in ['DiscordCanary','Discord']:
                            dataName = "Discord"
                            showplaying = False
                            openwindow = 'Ｃｈａｔｔｉｎｇ'
                            largeimage = 'talking'
                            largetext = 'Writing on Discord'

                        elif openwindow == 'opera':
                            dataName = "Internet"
                            showplaying = False
                            wakanimtest = openwindowtitle[-18:]
                            youtubetest = openwindowtitle.split(' - ')[-1][:-8][-7:]
                            #print(wakanimtest)
                            if  youtubetest == 'YouTube':
                                video = openwindowtitle[:-18]
                                image = "play"
                                
                                if video == '':
                                    image = None
                                    state = None
                                    largetext = 'https://www.youtube.com'
                                else:
                                    results = YoutubeSearch(f'"{video}"', max_results=1).to_json()
                                    parsedData = json.loads(results)["videos"][0]
                                    largetext = 'https://www.youtube.com'+parsedData["url_suffix"]
                                    state = f'{video} - {parsedData["channel"]}'

                                openwindow = f'📺: YouTube'
                                largeimage = 'youtube'
                            elif wakanimtest == 'Wakanim.TV – Opera':
                                video = openwindowtitle[:-38]
                                openwindow = '📺: Wakanim'
                                image = "play"
                                state = video
                                largetext = f'https://www.wakanim.tv/de/v2/'
                                largeimage = 'wakanim'
                            else:
                                openwindow = '🌐: Browsing the internet'
                                largeimage = 'internet'
                                largetext = 'Dial up to the Internet with CompuServe for 0.05$ per minute?'

                        elif openwindow == 'vivaldi':
                            dataName = "Internet"
                            showplaying = False
                            wakanimtest = openwindowtitle[-20:]
                            youtubetest = openwindowtitle.split(' - ')[-2]
                            #print(wakanimtest)
                            #print(openwindowtitle)
                            if  youtubetest == 'YouTube':
                                video = openwindowtitle[:-18]
                                image = "play"
                                
                                if video == '':
                                    image = None
                                    state = None
                                    largetext = 'https://www.youtube.com'
                                else:
                                    results = YoutubeSearch(f'"{video}"', max_results=1).to_json()
                                    parsedData = json.loads(results)["videos"][0]
                                    largetext = 'https://www.youtube.com'+parsedData["url_suffix"]
                                    state = f'{video} {parsedData["channel"]}'

                                openwindow = f'📺: YouTube'
                                largeimage = 'youtube'
                            elif wakanimtest == 'Wakanim.TV - Vivaldi':
                                video = openwindowtitle[:-40]
                                openwindow = '📺: Wakanim'
                                image = "play"
                                state = video
                                largetext = f'https://www.wakanim.tv/de/v2/'
                                largeimage = 'wakanim'
                            else:
                                openwindow = '🌐: Browsing the internet'
                                largeimage = 'internet'
                                largetext = 'Dial up to the Internet with CompuServe for 0.05$ per minute?'

                        elif openwindow in ['powershell','WindowsTerminal','cmd','Hyper']:
                            showplaying = False
                            openwindow = '🔐: Terminal'
                            largeimage = 'terminal'
                            largetext = 'In the Terminal...'
                            dataName = "Terminal"

                        elif openwindow == 'Terminus':
                            showplaying = False
                            openwindow = '🔐: SSH Connection to PI'
                            largeimage = 'terminal'
                            largetext = 'Talking to the Raspberry...'
                            dataName = "Terminal"

                        elif openwindow == 'Photoshop':
                            showplaying = False
                            largeimage = 'photoshop'
                            try:
                                openproject = openwindowtitle.split('@')[0]
                                openwindow = f'🖼️: {openproject}'
                            except Exception as e:
                                logError(e)
                                openwindow = '🖼️: Photoshop'                   
                            largetext = 'Editing an Image!'

                        elif openwindow == 'VALORANT-Win64-Shipping':
                            showplaying = False
                            openwindow = '🎮: VALORANT'
                            largeimage = 'valorant'
                            dataName = "Valorant"
                            ptime = readable.time(seconds=playtime.read(dataName), granularity=2, limit='h', language='en')
                            largetext = f'Tracked Time : {ptime} '

                        elif openwindow in ['WhatsApp','Ferdi']:
                            showplaying = False
                            openwindow = '📲: Writing on whatsapp...'
                            largeimage = 'whatsapp'
                            dataName = "Whatsapp"
                            largetext = '😹😺😸😻😼😽🙀😿'

                        elif openwindow == 'Mobalytics Desktop':
                            showplaying = False
                            openwindow = '⚡: Getting league stats/runes...'
                            largeimage = 'mobalytics'
                            largetext = 'Yasuo 0/10/0 Powerspike Runes'

                        elif openwindow == 'Blitz':
                            showplaying = False
                            openwindow = '⚡: Getting league stats/runes...'
                            largeimage = 'blitz'
                            largetext = 'Yasuo 0/10/0 Powerspike Runes'

                        elif openwindow == 'Spotify':
                            showplaying = False
                            openwindow = '🎶: Changing the music'
                            largeimage = 'bigspotify'
                            largetext = "You can see what I'm listening to if you hover over the small spotify icon!"
                            
                        elif openwindow == 'javaw':
                            showplaying = False
                            openwindow = '🎮: Minecraft'
                            largeimage = 'minecraft'
                            dataName = "Minecraft"
                            largetext = "Creeper, aw man!"
                            
                        elif openwindow == 'LockApp':
                            showplaying = False
                            openwindow = '💤 ⓐⓕⓚ 💤'
                            largeimage = 'locked'
                            dataName = "afk"
                            largetext = "Windows is locked and not in use."
                            
                        elif openwindow == 'Notion':
                            showplaying = False
                            openwindow = '📑: Organizing | Learning'
                            largeimage = 'notion'
                            dataName = "Notion"
                            largetext = "I really recommend you to try Notion tho if you like to keep things cleanly organized"

                        elif openwindow == 'Overcooked2':
                            showplaying = False
                            openwindow = '🎮: Overcooked! 2'
                            largeimage = 'overcooked2'
                            dataName = "Overcooked 2"
                            largetext = "PANICING"

                        elif openwindow == 'EpicGamesLauncher':
                            showplaying = False
                            openwindow = "🕹️: EpicGames"
                            largeimage = 'epicgames'
                            dataName = "Epic Games"
                            largetext = 'Browsing the Library...'

                        elif openwindow == 'BloonsTD6':
                            showplaying = False
                            openwindow = "🎮: BloonsTD 6"
                            dataName = "btd6"
                            largeimage = 'btd6'
                            largetext = None

                        elif openwindow == 'DeadByDaylight-Win64-Shipping':
                            showplaying = False
                            openwindow = "🎮: Dead by Daylight"
                            largeimage = 'deadbydaylight'
                            largetext = 'Dead by Daylight'
                            dataName = "Dead by Daylight"

                        elif openwindow == 'GalaxyClient':
                            showplaying = False
                            openwindow = "🕹️: Game Library"
                            largeimage = 'goggalaxy'
                            largetext = 'Deciding what game to play...'
                            dataName = "GOG Galaxy"

                        elif openwindow == 'WsaClient':
                            showplaying = False
                            if openwindowtitle == 'TikTok':
                                openwindow = "📺: TikTok"
                                largeimage = 'tiktok'
                                largetext = 'Scrolling through Tiktok'
                                dataName = "TikTok"
                            else:
                                openwindow = openwindowtitle
                                largeimage = 'wsa'
                                largetext = 'Android App'
                                dataName = "Android"

                        elif openwindow == 'valheim':
                            showplaying = False
                            openwindow = "🕹️: Valheim"
                            dataName = "Valheim"
                            largeimage = 'valheim'
                            largetext = 'Survival Game'

                    elif hidden: #if the hidden/afk mode is true
                        showplaying = False
                        openwindow = '💤 ⓐⓕⓚ 💤'
                        largeimage = 'afk'
                        dataName = "afk"
                        largetext = 'Not available on PC'

                    #limit if over 128 chars
                    largetext = largetext[:125] + (largetext[125:] and '...')
                    
                    #if it's a not defined window, display it this way:
                    if showplaying:
                        openwindow = '《'+openwindow+'》'

                    

                    #if anything changed, set update to True
                    needs_update = [globaldetails != openwindow, globalstate != statetext, globallarge_image != largeimage, globallarge_text != largetext, globalsmall_image != image, globalsmall_text != state]
                    if any(needs_update):
                        update = True


                    if dataName:
                        print(dataName+' '+str(looptime))
                        playtime.write(str(dataName), looptime)
                        
                    
                    #resets timer every time a new application is showed    
                    #if globaldetails != openwindow:
                        #start_time = time.time()

                    #if update is True, update the RPC
                    if update:
                        #update connection to rpc server with all detail
                        RPC.update(
                            details=openwindow, #currently open window name
                            state=statetext, #current cpu usage
                            large_image=largeimage, #set large image 
                            large_text=largetext, #set large image text
                            small_image=image, #set small image
                            small_text=state, #set small image text
                            buttons=[{
                                "label": "ʟᴀɴᴛᴇʀɴ.ʟᴏʟ", #set button label
                                "url": "https://Lantern.LoL" #set button link
                                }]
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
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logging.critical(e) #print error message(for debug)
                logging.critical(f'DEBUG : {exc_type} {fname} in line {exc_tb.tb_lineno}\n Resetting in 15 Seconds...') #print
                time.sleep(15) #wait 15 seconds
                reset()
    except Exception as e:
        logging.critical(e)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)