from tkinter.constants import TRUE
import PySimpleGUI as sg
import random
from collections import Counter
from PySimpleGUI.PySimpleGUI import WINDOW_CLOSED

#Layout ist nebeneinander weil übereinander nicht auf den Bildschirm passt
layout = [
            [sg.Text('0', size=(2, 1), key='-AUGEN1-', tooltip="Augen auf dem Würfel", background_color= 'white', text_color= 'black'),sg.Text('  '),
            sg.Text('0', size=(2, 1), key='-AUGEN2-', tooltip="Augen auf dem Würfel", background_color= 'white', text_color= 'black'),sg.Text('  '),
            sg.Text('0', size=(2, 1), key='-AUGEN3-', tooltip="Augen auf dem Würfel", background_color= 'white', text_color= 'black'),sg.Text('  '),
            sg.Text('0', size=(2, 1), key='-AUGEN4-', tooltip="Augen auf dem Würfel", background_color= 'white', text_color= 'black'),sg.Text('  '),
            sg.Text('0', size=(2, 1), key='-AUGEN5-', tooltip="Augen auf dem Würfel", background_color= 'white', text_color= 'black'),sg.Text('  '),
            sg.Button('Würfeln', size=(5, 2))]
            ,
            [sg.Checkbox('',size=(2, 1), key='-EINS-', tooltip='Anklicken um Würfel zu behalten.'),sg.Checkbox('',size=(2, 1), key='-ZWEI-', tooltip='Anklicken um Würfel zu behalten.'),sg.Checkbox('',size=(2, 1), key='-DREI-', tooltip='Anklicken um Würfel zu behalten.'),sg.Checkbox('',size=(2, 1), key='-VIER-', tooltip='Anklicken um Würfel zu behalten.'),sg.Checkbox('',size=(2, 1), key='-FÜNF-', tooltip='Anklicken um Würfel zu behalten.')]
            ,
            [sg.Text('Einser\t\t'), sg.Button('', size=(2, 1), key='1'), sg.Text('Dreierpasch\t'), sg.Button('', size=(2, 1), key='-3PASCH-')]
            ,
            [sg.Text('Zweier\t\t'), sg.Button('', size=(2, 1), key='2'), sg.Text('Viererpasch\t'), sg.Button('', size=(2, 1), key='-4PASCH-')]
            ,
            [sg.Text('Dreier\t\t'), sg.Button('', size=(2, 1), key='3'), sg.Text('Full House\t'), sg.Button('', size=(2, 1), key='-HOUSE-')]
            ,
            [sg.Text('Vierer\t\t'), sg.Button('', size=(2, 1), key='4'), sg.Text('Kleine Straße\t'), sg.Button('', size=(2, 1),key='-KLEINE-')]
            ,
            [sg.Text('Fünfer\t\t'), sg.Button('', size=(2, 1), key='5'), sg.Text('Große Straße\t'), sg.Button('', size=(2, 1), key='-GROSSE-')]
            ,
            [sg.Text('Sechser\t\t'), sg.Button('', size=(2, 1), key='6'), sg.Text('Kniffel\t\t'), sg.Button('', size=(2, 1), key='-KNIFFEL-')]
            ,
            [sg.Text('Summe\t\t'), sg.Button('0', size=(2, 1), key='-SUMME-'), sg.Text('Chance\t\t'), sg.Button('', size=(2, 1), key='-CHANCE-')]
            ,
            [sg.Text('Bonus\t\t'), sg.Button('35', size=(2, 1), key='-BONUS-', disabled=True),sg.Text('Summe rechts\t'), sg.Button('0', size=(2, 1), key='-RECHTS-')]
            ,
            [sg.Text('Summe mit Bonus\t'), sg.Button('0', size=(2, 1), key='-SMITBONUS-') ]
            ,           
            [sg.Text('----------------------------------------------', text_color= 'white')]
            ,
            [sg.Text('Summe gesamt\t'), sg.Button('', size=(2, 1), key='-GESAMT-', tooltip='Fertig? Drück mich!')]
        ]

fenster = sg.Window("Kniffel", layout, size=(400, 450), return_keyboard_events=True)
zahler = 0  #globale Variable zum überprüfen der Würfe (nicht mehr als drei, null bei jedem neuen Zug)
geworfen = () #globales Tuple das die gewürfelten Augenzahlen speichert
wieviel = 0 #globale Variable zum errechnen der anzurechnenden Punkte

def zahlen(event:str):
    '''Gibt den Buttons der linken Reihe den jeweils richtigen Wert (z.B. bei drei dreien werden alle 
    summmiert und der Event Button von Dreier wird mit 9 upgedatet. Ebenso bei jeder anderen
    Augenzahl'''
    global zahler
    global geworfen
    global wieviel
    for zahl in geworfen:
        if zahl == event:
            wieviel += int(zahl)
    fenster[event].Update(wieviel)
    fenster[event].update(disabled=True)
    summe(wieviel)
    '''Die nachfolgenden Anweisungen befinden sich am Ende jeder Buttonfunktion bei der Vorraussetzungen
    überprüft und Summen eingetragen werden müssen.'''
    fenster['Würfeln'].Update(disabled=False)#neuer Zug beginnt, Würfeln muss wieder möglich sein
    for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:#alle checkboxen werden geleert
        fenster[box].Update(False)
    for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:#alle Würfel werden zurückgesetzt
        fenster[würfel].update('0')
    zahler = 0#die variable zum zählen der würfe pro Zug wird zurückgesetzt
    '''mir ist beim kommentieren eingefallen, dasss ich die Anweisungen oben auch hätte in eine Funktion 
    auslagern können'''

def summe(x:int):
    '''Funktion zum errechnen der Summe aller Punkte der linken Seite'''
    y = fenster['-SUMME-'].GetText()
    z = int(y) + x
    fenster['-SUMME-'].update(z)

def summerechts(x:int):
    '''Funktion zum Errechnen der Summe aller Punkte der rechten Seite'''
    rechts = fenster['-RECHTS-'].GetText()
    c = int(rechts) + x
    fenster['-RECHTS-'].update(c)

def bonus():
    '''Funktion zum Enablen des Bonus Button falls die Summe der linken Reihe >= 63 ist'''
    y = int(fenster['-SUMME-'].GetText())
    if y >= 63:
        fenster['-BONUS-'].update(disable=False)
    fenster['-SMITBONUS-'].update(y + 35)

def pasch(z: int, event):
    #gibt die Summe aller Augen zurück falls ein Pasch geworfen wurde
    global geworfen
    global zahler
    x = 0
    a = Counter(geworfen)
    b = dict(a)#mit einem dictionary kann ich überprüfen ob irgendeine Augenzahl mehrfach vorhanden ist
    if z in b.values():
        for zahl, vorhanden in b.items():
            '''Alle Augen (zahl) werden so oft mal genommen wie sie vorhanden sind und alle
            Multiplikationsergebnisse werden zu x addiert'''
            x += (int(zahl)*int(vorhanden))
        fenster[event].update(disabled=True)
        fenster['Würfeln'].Update(disabled=False)
        for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
            fenster[box].Update(False)
        for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
            fenster[würfel].update('0')
        zahler = 0
    else:#falls die Augenzahlen die Anforderungen nicht erfüllen kann der Spieler das Feld streichen lassen
        
        antwort = sg.popup_yes_no('Soll dieses Feld gestrichen werden?')
        if antwort == 'Yes':
                    fenster[event].update('-')
                    fenster[event].update(disabled=True)
                    fenster['Würfeln'].update(disabled=False)
        else:
                    sg.Popup('Du hast aber keinen Pasch.')
            
    return x

def fullhouse():
    #Fullhouse? Wenn ja: 25 Punkte eintragen
    global geworfen
    global zahler
    a = Counter(geworfen)
    b = dict(a)
    if 2 in b.values() and 3 in b.values():#eine Augenzahl muss 2mal eine Augenzahl muss 3mal in geworfen sein
        fenster['-HOUSE-'].update('25')
        fenster['-HOUSE-'].update(disabled=True)
        summerechts(25)
        zahler = 0
        fenster['Würfeln'].Update(disabled=False)
        for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
            fenster[box].Update(False)
        for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
            fenster[würfel].update('0')
        
    else:
        antwort = sg.popup_yes_no('Soll dieses Feld gestrichen werden?')
        if antwort == 'Yes':
            fenster['-HOUSE-'].update('-')
            fenster['Würfeln'].update(disabled=False)
            fenster['-HOUSE-'].update(disabled=True)
        else:
            sg.Popup('Du hast aber kein Full House.')

def chance(x:tuple):
    global zahler
    #die chance wird am Häufigsten gestrichen, deswegen kommt zuerst die Frage
    antwort = sg.popup_yes_no('Soll dieses Feld gestrichen werden?')
    if antwort == 'Yes':
            fenster['-CHANCE-'].update('-')
            fenster['-CHANCE-'].update(disabled=True)
            fenster['Würfeln'].update(disabled=True)
            for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                fenster[box].Update(False)
            for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                fenster[würfel].update('0')
            zahler = 0

    if antwort == 'No':
            zahlen = []#um alle Augen als integer zu sammeln und einfacher zusammen zu rechnen
            for zahl in x:
                x = int(zahl)
                zahlen.append(x)
            z = sum(zahlen)
            fenster['-CHANCE-'].update(z)
            fenster['-CHANCE-'].update(disabled=True)
            fenster['Würfeln'].update(disabled=False)
            summerechts(z)
            for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                    fenster[box].Update(False)
            for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                    fenster[würfel].update('0')
            zahler = 0
        
def strassen(z: int, event):
    '''Diese Funktion überprüft ob überhaupt eine Straße geworfen wurde und wenn ja, welche.'''
    global zahler
    global geworfen
    strassentest = len(set(geworfen))
    '''Bei einem Set werden alle doppelten Werte entfernt, eine Große Straße kann keine Augen doppelt enthalten,
    eine kleine Straße nur ein Augenpaar. Die Länge eines Sets der geworfenen Augen gibt also Auskunft darüber 
    ob eine Straße geworfen wurde'''
    if z == 4 and strassentest >= z:
            fenster[event].update('30')
            fenster[event].update(disabled=True)
            fenster['Würfeln'].Update(disabled=False)
            summerechts(30)
            for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                fenster[box].Update(False)
            for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                fenster[würfel].update('0')
            zahler = 0
    elif z == 5 and strassentest == z:
            fenster[event].update('40')
            fenster[event].update(disabled=True)
            fenster['Würfeln'].Update(disabled=False)
            summerechts(40)
            for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                fenster[box].Update(False)
            for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                fenster[würfel].update('0')
            zahler = 0
    else:
            antwort = sg.popup_yes_no('Soll dieses Feld gestrichen werden?')
            if antwort == 'Yes':
                fenster[event].update('-')
                fenster[event].update(disabled=True)
                for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                    fenster[box].Update(False)
                for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                    fenster[würfel].update('0')
                zahler = 0

            else:
                if z == 4:
                    sg.popup('Du hast aber keine Kleine Straße.')
                else:
                    sg.popup('Du hast aber keine Große Straße')

def kniffel():
    '''Funktion testet ob ein Kniffel geworden wurde und updatet alle involvierten Buttons'''
    global zahler
    global geworfen
    kniffeltest = len(set(geworfen)) 
    if kniffeltest == 1:#ein kniffel enthält keine doppelten Augen
            fenster['-KNIFFEL-'].update('50')
            fenster[event].update(disabled=True)
            fenster['Würfeln'].update(disabled=False)
            summerechts(50)
            for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                fenster[box].Update(False)
            for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                fenster[würfel].update('0')
            zahler = 0
    else:
            antwort = sg.popup_yes_no('Soll dieses Feld gestrichen werden?')
            if antwort == 'Yes':
                fenster[event].update('-')
                fenster[event].update(disabled=True)
                fenster['Würfeln'].update(disabled=False)
                for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                    fenster[box].Update(False)
                for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                    fenster[würfel].update('0')
                zahler = 0

            else:
                sg.popup('Du hast aber keinen Kniffel.')

def gesamt():
    '''Funktion überprüft ob alle möglichen Würfe getätigt wurden und gibt dann
    die Gesamtpunktzahl zurück'''
    erledigt = 0
    for button in ['1', '2', '3', '4', '5', '6', '-BONUS-', '-3PASCH-', '-4PASCH-', '-HOUSE-', '-KNIFFEL-', '-CHANCE-','-KLEINE-', '-GROSSE-']:
        y = fenster[button].GetText()
        if y != '':
            erledigt += 1
            if erledigt == 14:
                a = int(fenster['-SMITBONUS-'].GetText())
                b = int(fenster['-SUMME-'].GetText())
                c = int(fenster['-RECHTS-'].GetText())
                if a != 0:
                    return (b+c)
                else:
                    return (a+c)
                
while True: #Beginn des Eventloops
    
    event, werte = fenster.read()
    y = int(fenster['-SUMME-'].GetText())
    if y >= 63:
        fenster['-BONUS-'].update(disabled=False)
        fenster['-SMITBONUS-'].update(y + 35)

    if event == sg.WINDOW_CLOSED or event == 'Escape:27':
        # Fenster schließen
        break
    if event == 'Würfeln' and zahler!= 3:
        wieviel = 0
        zahler += 1    
                
        würfelliste = ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']
        if werte['-EINS-']:
                würfelliste.remove('-AUGEN1-')
        if werte['-ZWEI-']:
                würfelliste.remove('-AUGEN2-')
        if werte['-DREI-']:
                würfelliste.remove('-AUGEN3-')
        if werte['-VIER-']:
                würfelliste.remove('-AUGEN4-')
        if werte['-FÜNF-']:
                würfelliste.remove('-AUGEN5-')  

        for würfel in würfelliste:
                fenster[würfel].update(random.randrange(1,7,1))
                (a, b, c, d, e) = (fenster['-AUGEN1-'].get(), fenster['-AUGEN2-'].get(), fenster['-AUGEN3-'].get(),fenster['-AUGEN4-'].get(),fenster['-AUGEN5-'].get())
                geworfen = (a, b, c, d, e)

    if zahler == 3:
            fenster['Würfeln'].Update(disabled=True)
            (a, b, c, d, e) = (fenster['-AUGEN1-'].get(), fenster['-AUGEN2-'].get(), fenster['-AUGEN3-'].get(),fenster['-AUGEN4-'].get(),fenster['-AUGEN5-'].get())
            geworfen = (a, b, c, d, e)
            
    if event in ['1', '2', '3', '4', '5', '6'] and event in geworfen:
        zahlen(event)

    if event == '-BONUS-':
        bonus()
        fenster[event].update(disabled=True)

    if event == '-3PASCH-':
        c = pasch(3, event)
        fenster['-3PASCH-'].update(c)
        summerechts(c)

    if event == '-4PASCH-':
        c = pasch(4, event)
        fenster['-4PASCH-'].update(c)
        summerechts(c)

    if event == '-HOUSE-':
        fullhouse()
    
    if event == '-KLEINE-':
        strassen(4, event)
    
    if event == '-GROSSE-':
        strassen(5, event)
    
    if event == '-KNIFFEL-':
        kniffel()
    
    if event == '-CHANCE-':
        chance(geworfen)

    if event == '-GESAMT-':
        x = gesamt()
        fenster[event].update(x)
        antwort = sg.popup_yes_no('Noch ein Spiel?')
        if antwort == 'Yes':
            for button in ['1', '2', '3', '4', '5', '6', '-3PASCH-', '-4PASCH-', '-HOUSE-', '-KNIFFEL-', '-CHANCE-','-KLEINE-', '-GROSSE-', '-SUMME-', '-RECHTS-', '-GESAMT-', '-SMITBONUS-']:
                if button in ['-SUMME-','-RECHTS-']:
                        fenster[button].update('0')
                        for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                            fenster[box].Update(False)
                        for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                            fenster[würfel].update('0')
                        zahler = 0
                        fenster['Würfeln'].update(disabled=False)
                else:
                    fenster[button].update('')
                    fenster[button].update(disabled=False)
                    for box in ['-EINS-','-ZWEI-','-DREI-','-VIER-', '-FÜNF-']:
                        fenster[box].Update(False)
                    for würfel in ['-AUGEN1-','-AUGEN2-','-AUGEN3-','-AUGEN4-','-AUGEN5-']:
                        fenster[würfel].update('0')
                    zahler = 0
        else:
            fenster.close()

fenster.close()