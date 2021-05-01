#imports
import psutil #get hardware data
import threading #run multiple loops
import time #sleep
import win32gui #get focussed window
import win32process #get focussed window
import module.yasuo as yas #custom module for client data
import os, sys #restart script occasionally
from pynput import keyboard #check for hotkey
from pypresence import Presence #check for hotkey
from SwSpotify import spotify #get playing track info
from win10toast import ToastNotifier #push desktop notifications


#DEFAULTING
icon_path = "/secret.ico"
toast = ToastNotifier()
hidden = False
global globaldetails,globalstate,globallarge_image,globallarge_text,globalsmall_image,globalsmall_text
globaldetails = None
globalstate = None
globallarge_image = None
globallarge_text = None
globalsmall_image = None
globalsmall_text = None
start_time = time.time()
#DEFAULTING END

#hotkey listening loop
def hotkeylistener():

    #if hotkey got pressed
    def on_hotkey():
        print('hotkey pressed')
        global hidden
        if hidden is True: #set hidden variable to False if it's already True and give Windows notification
            toast.show_toast("rpc.pyw","no longer afk!",duration=3,icon_path=icon_path,threaded=True)
            hidden = False
        elif hidden is False: #set hidden variable to True if it's already False and give Windows notification
            toast.show_toast("rpc.pyw","now afk!",duration=3,icon_path=icon_path,threaded=True)
            hidden = True

    #on keypress check if hotkey is pressed
    def on_press(key):
        return lambda k: key(l.canonical(k))

    hotkey = keyboard.HotKey(keyboard.HotKey.parse('1+='),on_hotkey)

    with keyboard.Listener(
            on_press=on_press(hotkey.press),
            on_release=on_press(hotkey.release)) as l:
        l.join()

def resettimer():
    time.sleep(900)
    if hidden is False:
        os.execv(sys.executable, ['pyw'] + sys.argv)

#thread hotkeylistener and timer
hkListener = threading.Thread(target=hotkeylistener)
rTimer = threading.Thread(target=resettimer)
rTimer.start()
hkListener.start()

while True:
    try:
        
        #connect to application via id on pipe 0
        client_id = '828958778866270238' #set discord application id
        RPC = Presence(client_id,pipe=0) #set the client with id and define what pipe
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
                image = "heart"
                state = "Λ 24.02.2020"
                statetext = None #"𝗖𝗣𝗨: "+str(cpu_per)+"%"
                largetext = "The open program has no set Image"
                largeimage = "unknown"

            #get process id
            w=win32gui #shortversion
            w.GetWindowText (w.GetForegroundWindow()) #get ForegroundWindow
            pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow()) #get ForegroundWindow ID
            openwindow = psutil.Process(pid[-1]).name() #get the window name through the ID
            openwindow = openwindow[:-4] #remove .exe
            showplaying = True #default to True

            #if its not hidden
            if not hidden:
                
                #if the window is League of Legends, get all data thats needed and use it
                if openwindow == 'League of Legends':
                    
                    if playing == False:
                         statetext = "hover over the to see stats"

                    #get ingame data
                    me = yas.get_currentuser() #set me as my league username
                    friends = ['llReaper','Glennie101','Wallecho','Sturmi101','Sayji','Ahrier69','L9 Rawnip','LetsGameDanny','Yumα'] #list with friends usernames
                    mode = yas.get_currentmode() #get current league gamemode 
                    champion = yas.get_clientdata(me,'champion') #get my current champion
                    kda = yas.get_clientdata(me,'kda') #get my kda
                    cs = yas.get_clientdata(me,'cs') #get my cs
                    visionscore = yas.get_clientdata(me,'vision') #get my vision score
                    gametime = yas.get_clientdata(me,'time') #get the current gametime

                    #visuals
                    showplaying = False
                    openwindow = '𝚃𝚒𝚕𝚝 𝚘𝚏 𝙻𝚎𝚐𝚎𝚗𝚍𝚜'
                    largeimage = 'leagueingame'

                    #set text
                    friendsingame = [] #create a list

                    for friend in friends: #for each friend in the list of friends usernames
                        if yas.check_playeringame(friend): #check if the friend is in my game
                            friendsingame.append(friend) # add the friend to the list 
                            
                    if me in friendsingame:
                        friendsingame.remove(me)
                        
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
                                
                #all other elif's for checking if a window is a customized one and if it is, take different name,image,and imagetext and say that its a defined window
                elif openwindow == 'Code':
                    showplaying = False
                    openwindow = 'vsCode'
                    largeimage = 'vscode'
                    largetext = "if str(life.activity) in list_shit_things :\n os.startfile('LeagueOfLegends')"

                elif openwindow == 'explorer':
                    showplaying = False
                    openwindow = 'Looking through files...'

                elif openwindow == 'LeagueClientUx':
                    showplaying = False
                    openwindow = 'League Lobby'
                    largeimage = 'leaguelobby'
                    largetext = 'Looking to play a game..'

                elif openwindow == 'RiotClientUx':
                    showplaying = False
                    openwindow = 'logging in...'
                    largeimage = 'riotclient'
                    largetext = 'User: YumaIsBack\nPassword: deggubkcitS'

                elif openwindow in ['DiscordCanary','Discord']:
                    showplaying = False
                    openwindow = 'Ｃｈａｔｔｉｎｇ'
                    largeimage = 'talking'
                    largetext = 'Writing on Discord'

                elif openwindow == 'brave':
                    showplaying = False
                    openwindow = 'Browsing the internet'
                    largeimage = 'internet'
                    largetext = 'Dial up to the Internet with CompuServe for 0.05$ per minute?'

                elif openwindow in ['powershell','WindowsTerminal','cmd','Hyper']:
                    showplaying = False
                    openwindow = '《Terminal》'
                    largeimage = 'terminal'
                    largetext = 'In the Terminal...'

                elif openwindow == 'Terminus':
                    showplaying = False
                    openwindow = '《SSH Connection to PI》'
                    largeimage = 'terminal'
                    largetext = 'Talking to the Raspberry...'

                elif openwindow == 'Photoshop':
                    showplaying = False
                    openwindow = '《Photoshop》'
                    largeimage = 'photoshop'
                    largetext = 'Editing an Image!'

                elif openwindow == 'VALORANT-Win64-Shipping':
                    showplaying = False
                    openwindow = '𝗽𝗹𝗮𝘆𝗶𝗻𝗴: VALORANT'
                    largeimage = 'valorant'
                    largetext = 'Aimbot.exe'

                elif openwindow == 'WhatsApp':
                    showplaying = False
                    openwindow = 'writing on whatsapp...'
                    largeimage = 'whatsapp'
                    largetext = '😹😺😸😻😼😽🙀😿'

                elif openwindow == 'Mobalytics Desktop':
                    showplaying = False
                    openwindow = 'Getting league stats/runes...'
                    largeimage = 'mobalytics'
                    largetext = 'Yasuo 0/10/0 Powerspike Runes'

                elif openwindow == 'Blitz':
                    showplaying = False
                    openwindow = 'Getting league stats/runes...'
                    largeimage = 'blitz'
                    largetext = 'Yasuo 0/10/0 Powerspike Runes'

                elif openwindow == 'Spotify':
                    showplaying = False
                    openwindow = 'Changing the music'
                    largeimage = 'bigspotify'
                    largetext = "You can see what I'm listening to if you hover over the small spotify icon!"

            elif hidden: #if the hidden/afk mode is true
                showplaying = False
                openwindow = '💤 ⓐⓕⓚ 💤'
                largeimage = 'afk'
                largetext = 'Not available on PC'

            #limit if over 128 chars
            largetext = largetext[:125] + (largetext[125:] and '...')
            
            #if it's a not defined window, display it this way:
            if showplaying:
                openwindow = '《'+openwindow+'》'

            #if anything changed, set update to True
            needs_update = [globaldetails != openwindow, globalstate != statetext, globallarge_image != largeimage, globallarge_text != largetext, globalsmall_image != image, globalsmall_text != state]
            if any(needs_update):
                update=True
            
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
                        "label": "𝖕𝖗𝖔𝖋𝖎𝖑𝖊", #set button label
                        "url": "https://discord.bio/p/yumaa" #set button link
                        }]
                    )

                #set the last update to check in the next loop
                globaldetails = openwindow
                globalstate = statetext
                globallarge_image = largeimage
                globallarge_text = largetext
                globalsmall_image = image
                globalsmall_text = state

            #wait 15 seconds then repeat the loop
            time.sleep(15)
            
            
                
    #if an error occurs while running the loop (mostly rpc not being able to connect to discord due to discord being closed)
    except Exception as e:
        print(e) #print error message(for debug)
        print('DEBUG : failed to connect to discord...\nTrying again in 15s') #print
        time.sleep(15) #wait 15 seconds
