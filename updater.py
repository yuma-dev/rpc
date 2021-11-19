from tqdm import tqdm
import requests,shutil,time,os,urllib.request,ctypes,sys,psutil
aboutUrl = "https://raw.githubusercontent.com/yuma-dev/rpc/main/about.txt"
file = urllib.request.urlopen(aboutUrl)


def is_running(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
def closeRPC():
    if is_running("pythonw.exe"):
        rpcOpen = True
        inp = input("CLOSE pythonw.exe(probably rpc) BEFORE UPDATING!\nClose? [Y/N]\n \nUSER: ")
        if inp.lower() == 'y':
            os.system('py killrpc.py')
            print('Closing...')
            while rpcOpen:
                if is_running("pythonw.exe"):
                    rpcOpen = True
                    time.sleep(0.5)
                    
                else:
                    rpcOpen = False
                    print('closed!')
                    return
        else:
            exit()

closeRPC()

for line in file:
    line = line.decode("utf-8")
    if line.split("=")[0] == "VERSION":
        rawCloudVersion = line.split("=")[1]
        cloudVersion = line.split("=")[1].replace(".", "")

with open(os.getcwd()+"\\"+'about.txt', "r") as file:
    for line in file:
        if line.split("=")[0] == "VERSION":
            rawBaseVersion = line.split("=")[1]
            baseVersion = line.split("=")[1].replace(".", "")

def moduleDownloads():
    import os,time,sys
    url = 'https://raw.githubusercontent.com/yuma-dev/rpc/main/modules.txt'
    try:
        import urllib.request
        print("imported urllib.request")
    except ImportError:
        print("importerror urllib")
        os.system('py -m pip install urllib')
        input('Installed important script, please restart')
    modules = urllib.request.urlopen(url).readlines()
    try:
        for line in modules:
            
            module = line.decode('utf-8').strip()

            exec("import "+module)
            print("alread installed "+module)
    except Exception as e:
        os.system('py -m pip install --upgrade setuptools')
        print(e)
        for line in modules:
            module = line.decode('utf-8').strip()
            if module == 'wx':
                module = 'wxpython'
            print("installing "+module)
            os.system(f"py -m pip install {module}")

        
        input('Neue Module wurden installiert, das script bitte neustarten...')
        exit()

def killRpc():
    os.system("taskkill /IM pythonw.exe /F")

def Update():
    changelog = None
    killRpc()
    moduleDownloads()
    os.mkdir("temp")


    for file in os.listdir(os.getcwd()+"\\"+"modules"):
        
        if file in ['customAddons.py']:
            print(f"Moving {file} to temp")
            os.rename(os.getcwd()+"\\modules\\"+file, os.getcwd()+"\\temp\\"+file)
            time.sleep(0.1)

    for file in os.listdir(os.getcwd()+"\\"+"data"):
        
        if file in ['database.json','config.ini']:
            print(f"Moving {file} to temp")
            os.rename(os.getcwd()+"\\data\\"+file, os.getcwd()+"\\temp\\"+file)
            time.sleep(0.1)


    for file in os.listdir(os.getcwd()):
        if file not in ['temp', 'updater.py', 'installer.py']:
            try:
                os.remove(file)
                print(f"Removed {file}")
            except Exception:
                shutil.rmtree(file)
                print(f"Removed {file}")
            time.sleep(0.1)


    url = 'https://github.com/yuma-dev/rpc/archive/refs/heads/main.zip'
    response = requests.get(url, stream=True)
    with open("main.zip", "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    print('Downloaded RPC!')


    time.sleep(0.3)
    print('Unpacking...')
    shutil.unpack_archive('main.zip')
    print('Unpacked!')
    os.remove("main.zip")
    time.sleep(0.3)


    for file in os.listdir(os.getcwd()+"\\rpc-main"):
        if file in ['README.md','updater.py','changelog.txt','modules.txt']:

            if file == 'changelog.txt':

                with open(os.getcwd()+"\\rpc-main\\"+file,'r') as f:
                    changelogVersion = f.readline().rstrip()
                    print(changelogVersion)
                    if changelogVersion > rawBaseVersion:
                        changelog = f.read()

                print(f"Removing {file}")
                os.remove(os.getcwd()+"\\rpc-main\\"+file)
                time.sleep(0.3)



            else:
                if file not in ['changelog.txt']:
                    print(f"Removing {file}")
                    os.remove(os.getcwd()+"\\rpc-main\\"+file)
                    time.sleep(0.1)

        else:

            print(f"Moving {file}")
            time.sleep(0.3)
            os.rename(os.getcwd()+"\\rpc-main\\"+file, os.getcwd()+"\\"+file)
            time.sleep(0.1)


    print(f"Removing rpc-main")
    os.rmdir(os.getcwd()+"\\rpc-main")


    print('Removing downloaded customAddons')    
    for file in os.listdir(os.getcwd()+"\\modules"):
        if file in ['customAddons.py']:
            os.remove(os.getcwd()+"\\modules\\"+file)
            time.sleep(0.1)


    print('Removing downloaded database and config')    
    for file in os.listdir(os.getcwd()+"\\data"):
        if file in ['database.json', 'config.ini']:
            os.remove(os.getcwd()+"\\data\\"+file)
            time.sleep(0.1)


    print('Moving saved customAddons.py and database back')
    for file in os.listdir(os.getcwd()+"\\temp"):
        if file in ['customAddons.py']:
            print(f"Moving {file} from temp")
            os.rename(os.getcwd()+"\\temp\\"+file, os.getcwd()+"\\modules\\"+file)
            time.sleep(0.1)
        if file in ['database.json','config.ini']:
            print(f"Moving {file} from temp")
            os.rename(os.getcwd()+"\\temp\\"+file, os.getcwd()+"\\data\\"+file)
            time.sleep(0.1)


    os.rmdir('temp')
    print('Removing temp files')


    if changelog:
        input(f' \n \n \n \nv{rawCloudVersion} Changelog:\n'+changelog)
        exit()
    

if cloudVersion > baseVersion:
    input(f'Github Version : {rawCloudVersion}\nLocal Version : {rawBaseVersion}\nUpdate available, do you want to update?\n  \n  \nPress enter to update...')

    Update()
    input('Done!')
    os.system('cls')

else:
    input('No update available...')