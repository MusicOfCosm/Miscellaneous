import winsound #Only supports wav sound format
from random import *
import time

note_acoustic = ['Do4.wav', 'Ré4.wav', 'Mi4.wav', 'Fa4.wav', 'Sol4.wav', 'La4.wav', 'Si4.wav']
note_beep = [ 131 ,  147 ,  165 ,  175 ,  196  ,  220 ,  247 ,  262 ,  294 ,  330 ,  349 ,  392  ,  440 ,  494]
notes = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si', 'Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']
note_name = ['Do3', 'Ré3', 'Mi3', 'Fa3', 'Sol3', 'La3', 'Si3', 'Do4', 'Ré4', 'Mi4', 'Fa4', 'Sol4', 'La4', 'Si4']

style = False
while not style:
    mode = input('Beep or Acoustic? ')

    if mode.lower() == 'beep':
        style = True
    
    elif mode.lower() == 'acoustic':
        style = True

    else:
        print('Not a valid answer!\n\n')


print('\n\n\nIf you want to listen to the note again, type "replay".\nIf you want to stop, type "quit" or "stop".')
Testing = True
while Testing:
    if mode.lower() == 'acoustic':
        note = randint(0, 6)
        winsound.PlaySound(note_acoustic[note], winsound.SND_FILENAME)
    if mode.lower() == 'beep':
        note = randint(0, 13)
        winsound.Beep(note_beep[note], 1000)
    
    answered = False
    while not answered:
        answer = input('\n\nWhat note do you think that was? ')
        
        if answer.lower() == notes[note].lower():
            print('Correct!')
            time.sleep(1.5)
            answered = True

        elif answer.lower() == 'replay':
            if mode.lower() == 'acoustic':
                winsound.PlaySound(note_acoustic[note], winsound.SND_FILENAME)
            if mode.lower() == 'beep':
                winsound.Beep(note_beep[note], 1000)
            answered = False

        elif answer.lower() == 'quit' or answer.lower() == 'stop':
            Testing = False
            answered = True

        else:
            print(f'Incorrect...\nIt was a {note_name[note]}!')
            time.sleep(1.5)
            answered = True