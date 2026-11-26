#libraries
from just_playback import Playback #kerner player
from tinytag import TinyTag #Music Tags
from pathlib import Path #Path
import time #Sleep
import sys # exit
#Files
from config import configuration
from TUI import drawer
from Core import functions
from Core import keybinding
#Text
program_name = "---Sunset player---"


Folder = Path(configuration.Folder).expanduser()
functions.check_OS()
import curses
#Control variables
current_index = 0
finished = False
index_music = 0 
has_folder = True

player = functions.get_player()
#list of music
music_list = functions.get_music_list(Folder)
non_shuffled = functions.deepest_copy(music_list)

#Functions
def playing(stdscr):

    #make global this var.
    global is_paused
    global program_name
    global index_music
    global player
    global non_shuffled
    global music_list

    #curses setup
    drawer.setup_drawers(stdscr)
    stdscr.nodelay(True)
    curses.curs_set(0)
    audio_settings = [False, False] #Is_paused, is_shuffle
    while True:
        #Turn on music & play
        functions.LAP(player, music_list, index_music)
        music, author, folder = functions.get_tags(music_list[index_music], Folder)
        args_for_print = [program_name, music, author, folder, audio_settings, player]
        drawer.draw_information(stdscr, *args_for_print)
        
        #Interact 
        while player.active != False or audio_settings[0]:

            music, author, folder = functions.get_tags(music_list[index_music], Folder)
            args_for_print = [program_name, music, author, folder, audio_settings, player]
            drawer.draw_information(stdscr, *args_for_print)

            time.sleep(0.1)
            
            try:
                key = stdscr.get_wch()
            except curses.error:
                key = None

            if key in keybinding.keys[0]:
                audio_settings[0] = not(audio_settings[0])
                if audio_settings[0] == True:
                    functions.Pause(player)
                else:
                    functions.Resume(player)

            if key in keybinding.keys[1] and not(audio_settings[0]):
                index_music -= 2
                break

            if key in keybinding.keys[2] and not(audio_settings[0]):
                break
            if key in keybinding.keys[3] :
                audio_settings[1] = not(audio_settings[1])
                if audio_settings[1]:
                    current_index = index_music
                    music_name = music_list[index_music]
                    music_list = functions.Shuffle(music_list)
                    index_music = music_list.index(music_name)          
                else:
                    music_name = music_list[index_music]
                    music_list = non_shuffled.copy()   
                    index_music = music_list.index(music_name)  
            if key in keybinding.keys[4]:
                sys.exit()
        player.stop()
        index_music = (index_music+1) % len(music_list)

#Checking if main.py is a main file
if __name__ == "__main__":
    curses.wrapper(playing)