import requests
import warnings
warnings.filterwarnings('ignore')

def get_currentmode():
    try:
        allrespones = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False).json()
        gamemode = allrespones['gameData']['gameMode']
        return gamemode 
    except Exception:
        return None

def get_currentuser():
    try:
        username = requests.get('https://127.0.0.1:2999/liveclientdata/activeplayername', verify=False).json()
        return username
    except Exception:
        return None

def get_clientdata(name, type):
    try:
        allrespones = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False)
        for players in allrespones.json()['allPlayers']:
            if players['summonerName'] == name:
                kills = players['scores']['kills']
                deaths = players['scores']['deaths']
                assists = players['scores']['assists']
                creepscore = players['scores']['creepScore']
                visionscore = round(players['scores']['wardScore'])
                kda = f'{kills}/{deaths}/{assists}'
                champion = players['championName']
                time = str(round(int(allrespones.json()['gameData']['gameTime'])/60,2)).replace('.', ':')
                gamemode = allrespones.json()['gameData']['gameMode']
                try:
                    skinname = players['skinName']
                except Exception:
                    skinname = None
                gold = round(allrespones.json()['activePlayer']['currentGold'])
                if type == 'kda':
                    return kda
                elif type == 'champion':
                    return champion
                elif type == 'time':
                    return time
                elif type == 'skinname':
                    return skinname
                elif type == 'gold':
                    return gold
                elif type in ['creepscore','cs']:
                    return creepscore
                elif type in ['visionscore','vision','vs']:
                    return visionscore
                else:
                    raise AttributeError('type is unknown')
    except Exception:
        return None

def check_playeringame(name):
    try:
        allrespones = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False)
        for players in allrespones.json()['allPlayers']:
            if players['summonerName'] == name:
                return True
        return False
    except Exception:
        return False
