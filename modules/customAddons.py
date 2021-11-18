

def getData(openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying): #in ruhe lassen!
    openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying=openwindow,openwindowtitle,playing,dataName,largeimage,largetext,state,image,showplaying

    print('in customAddons: %s' % openwindow)

    """
    Dieses Modul ist für eigene Programme
    Die daten die du bekommst: 

    openwindow = Dateiname des Programms ohne .exe (zbs. VALORANT-Win64-Shipping)
    openwindowtitle = Fenstertitel des Programms
    playing = spielt gerade Musik auf Spotify, True oder False



    Was du festlegen wirst :

    showplaying = immer False
    openwindow = Was wird als offenes Programm angezeigt?
    dataName = Wie wird es in der lokalen Datenbank aufgezeichnet? (NIEMALS NONE)
    largeimage = Name des großen bildes in der Datenbank 
    largetext = Text der angezeigt wird wenn du das große Bild hoverst
    image = Name des kleinen bildes in der Datenbank 
    state = Text der angezeigt wird wenn du das kleine Bild hoverst
    """

    
    if openwindow == 'Test':
        showplaying = False
        openwindow = None
        largeimage = None
        largetext = None
        image = None
        state = None
        

    elif openwindow == 'Test2':
        showplaying = False
        openwindow = None
        largeimage = None
        largetext = None
        image = None
        state = None
        
    

    return openwindow,dataName,largeimage,largetext,state,image,showplaying #in ruhe lassen!