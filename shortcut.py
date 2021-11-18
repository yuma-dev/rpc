import os, winshell, win32com.client
import win32com

autostart = winshell.startup()
here = os.getcwd()
#desktop = r"path to where you wanna put your .lnk file"

path = os.path.join(autostart, 'Discord Rich Presence Start.lnk')
target = os.getcwd()+"\\rpc.pyw"
icon = os.getcwd()+"\\rpc.pyw"

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.IconLocation = icon
shortcut.save()