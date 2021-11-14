import logging
import sys
class LogFile(object):
    """File-like object to log text using the `logging` module."""

    def __init__(self, name=None):
        self.logger = logging.getLogger(name)

    def write(self, msg, level=logging.INFO):
        self.logger.log(level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()
sys.stdout = LogFile('stdout')
sys.stderr = LogFile('stderr')
try:
    #imports
    import wx.adv #tray
    import wx #tray
    from ctypes import windll
    import psutil #get hardware data
    import threading #run multiple loops
    import time #sleep
    import win32gui #get focussed window
    import win32process #get focussed window
    import yasuo as yas #custom module for client data
    import os #restart script occasionally
    import traceback #get tracebacks for logs
    import json #get json data
    import readable #make things readable
    import playtime #get playtime data
    from datetime import datetime #get the current time for logging errors
    from pynput import keyboard #check for hotkey
    from pypresence import Presence #update local discord rich presence
    from SwSpotify import spotify #get playing track info
    from win10toast import ToastNotifier #push desktop notifications
    import tkinter as tk
    from youtube_search import YoutubeSearch #get youtube search info

    #DEFAULTING
    icon_path = "C:/Users/Fabi/Documents/rpc/secret.ico"
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
    TRAY_TOOLTIP = 'RPC' 
    TRAY_ICON = 'secret.ico'
    logging.basicConfig(level=logging.DEBUG, filename='logging.log', format = '%(asctime)s | %(levelname)s  -  %(message)s')
    #DEFAULTING END

    def create_menu_item(menu, label, func):
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item


    class TaskBarIcon(wx.adv.TaskBarIcon):
        def __init__(self, frame):
            self.frame = frame
            super(TaskBarIcon, self).__init__()
            self.set_icon(TRAY_ICON)
            self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

        def CreatePopupMenu(self):
            menu = wx.Menu()
            create_menu_item(menu, 'Restart', self.on_restart)
            menu.AppendSeparator()
            create_menu_item(menu, 'Show Logs', self.on_logs)
            menu.AppendSeparator()
            create_menu_item(menu, 'Toggle AFK', self.on_afk)
            menu.AppendSeparator()
            create_menu_item(menu, 'Exit', self.on_exit)
            return menu

        def set_icon(self, path):
            icon = wx.Icon(path)
            self.SetIcon(icon, TRAY_TOOLTIP)

        def on_left_down(self, event):      
            logging.info('Tray icon was left-clicked.')

        def on_restart(self, event):
            toast.show_toast("rpc.pyw","restarting!",duration=3,icon_path=icon_path,threaded=True)
            time.sleep(1)
            os.execv(sys.executable, ['pyw'] + sys.argv)

        def on_afk(self, event):
            hiddenText = "pressed"
            toggleHidden()

        def on_logs(self, event):
            root = tk.Tk()
            T = tk.Text(root, height=60, width=100)
            T.pack()
            with open(r'C:\Users\Fabi\Documents\rpc\logging.log', 'r') as logs:
                for line in logs.readlines():
                    T.insert(tk.END, line)
            tk.mainloop()

        def on_exit(self, event):
            wx.CallAfter(self.Destroy)
            self.frame.Close()
            raise SystemExit

    class App(wx.App):
        def OnInit(self):
            frame=wx.Frame(None)
            self.SetTopWindow(frame)
            TaskBarIcon(frame)
            logging.info("Started Tray Icon")
            return True

    def startTray():
        app = App(False)
        app.MainLoop()

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

    startTray()

    #thread hotkeylistener and timer
    rTimer = threading.Thread(target=resettimer)
    rTimer.start()

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
                pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow()) #get ForegroundWindow ID
                openwindow = psutil.Process(pid[-1]).name() #get the window name through the ID
                openwindow = openwindow[:-4] #remove .exe
                openwindowtitle = w.GetWindowText(w.GetForegroundWindow())
                showplaying = True #default to True
                dataName = openwindow

                #if its not hidden
                if not hidden:
                    
                    #if the window is League of Legends, get all data thats needed and use it
                    if openwindow == 'League of Legends':
                        
                        if playing == False:
                            statetext = "hover the pic for stats"
                            image = "lolsearch"

                        #get ingame data
                        me = yas.get_currentuser() #set me as my league username
                        friends = ['Sαyuri','Glennie101','Wallecho','Sturmi101','Sayji','Ahrier69','Takrα','LetsGameDanny','Yumα'] #list with friends usernames
                        mode = yas.get_currentmode() #get current league gamemode 
                        champion = yas.get_clientdata(me,'champion') #get my current champion
                        kda = yas.get_clientdata(me,'kda') #get my kda
                        cs = yas.get_clientdata(me,'cs') #get my cs
                        visionscore = yas.get_clientdata(me,'vision') #get my vision score
                        gametime = yas.get_clientdata(me,'time') #get the current gametime

                        #visuals
                        showplaying = False
                        openwindow = '🎮: 𝚃𝚒𝚕𝚝 𝚘𝚏 𝙻𝚎𝚐𝚎𝚗𝚍𝚜'
                        largeimage = 'leagueingame'

                        #set text
                        friendsingame = [] #create a list

                        for friend in friends: #for each friend in the list of friends usernames
                            if yas.check_playeringame(friend): #check if the friend is in my game
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
                            logging.error("in VS CODE : "+e)
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
                            logging.error("in Photoshop : "+e)
                            openwindow = '🖼️: Photoshop'                   
                        largetext = 'Editing an Image!'

                    elif openwindow == 'VALORANT-Win64-Shipping':
                        showplaying = False
                        openwindow = '🎮: VALORANT'
                        largeimage = 'valorant'
                        largetext = 'Aimbot.exe'
                        dataName = "Valorant"

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

                if openwindow.startswith("🎮: "):
                    image = None

                #if anything changed, set update to True
                needs_update = [globaldetails != openwindow, globalstate != statetext, globallarge_image != largeimage, globallarge_text != largetext, globalsmall_image != image, globalsmall_text != state]
                if any(needs_update):
                    update = True


                if dataName:
                    playtime.write(dataName, looptime)
                    lolSekunden = playtime.read("League of Legends")
                    readable.time(lolSekunden)
                
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
            with open("log.txt", "a") as log:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                log.write(f"{dt_string} {exc_type} {fname} in line {exc_tb.tb_lineno} : {str(e)}" + "\n")
            logging.critical(e) #print error message(for debug)
            logging.critical(f'DEBUG : {exc_type} {fname} in line {exc_tb.tb_lineno} ...\nRestarting in 15s') #print
            time.sleep(15) #wait 15 seconds
            reset()
except Exception as e:
    logging.error(e)
