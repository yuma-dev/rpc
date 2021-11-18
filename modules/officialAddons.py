from modules import yasuo,playtime,readable
from youtube_search import YoutubeSearch
import json

def getData(openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying):
    openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying = openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying
    print('in officialAddons: %s' % openwindow)


    #if the window is League of Legends, get all data thats needed and use it
    if openwindow == 'League of Legends':
        dataName = "League of Legends"
        
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
            openwindow = 'vsCode'
        largeimage = 'vscode'
        largetext = "if str(life.activity) in shitThings :\n os.startfile('LeagueOfLegends.exe')"

    elif openwindow == 'explorer':
        showplaying = False
        openwindow = '📁: Explorer'

    elif openwindow == 'LeagueClient':
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
            openwindow = '🖼️: Photoshop'                   
        largetext = 'Editing an Image!'

    elif openwindow == 'VALORANT-Win64-Shipping':
        showplaying = False
        openwindow = '🎮: VALORANT'
        largeimage = 'valorant'
        dataName = "Valorant"
        if playtime.read(dataName):
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


    return openwindow,dataName,largeimage,largetext,state,image,showplaying #in ruhe lassen!