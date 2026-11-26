#Define libraries
import sys
from pathlib import Path
from just_playback import Playback
from tinytag import TinyTag
from copy import deepcopy
import platform 
from random import shuffle
#Setup functions
def check_OS():
    try:
        import curses
    except:
        if platform.system() == "Windows":
            print("Download windows-curses using pip")
            print("pip install windows-curses")
            sys.exit()
        else:
            raise
def get_music_list(folder):
    music_list = []
    for music in folder.iterdir():
        if music.is_file() and music.suffix.lower() in [".mp3", ".flac", ".ogg", ".wav", ".m4a"]:
            music_list.append(music)

    if not music_list:
        print("Error: No music files found, or the folder path is invalid.")
        print("Advice: Check configuration.py file!")
        sys.exit()

    return music_list
def deepest_copy(folder):
    return deepcopy(folder)
#Graphics
def get_tags(music, Folder):
    tags = TinyTag.get(str(music))
    current_music = str("Now playing: " + f"{tags.title or music.name}")
    current_Author = str("Author: " + f"{tags.artist or "author that you may know"}")
    current_Folder = str("From folder: " + f"{str(Folder)}")
    return current_music, current_Author, current_Folder

#Audio
def get_player():
    player = Playback()
    return player

def LAP(player, list: list, index: int): #load_and_play
    player.load_file(str(list[index]))

    player.play()

def Pause(player):
    player.pause()
def Resume(player):
    player.resume()

def Shuffle(music_list):
    shuffle(music_list)
    return music_list