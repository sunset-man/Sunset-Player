import curses
from config import configuration
import just_playback

UI_mode = configuration.UI_mode
instruction = "[x]-Pause | [z]-Prev | [c]-Next | [s]-Shuffle | [q]-Quit"
Minimal = [10, 4]

def setup_drawers(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    curses.init_pair(2, curses.COLOR_MAGENTA, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)  
    curses.init_pair(5, curses.COLOR_BLUE, -1)  

def cut_and_replace(string: str, max_width):
    if len(string) <= max_width:
        return string
    else:
        if max_width <= 3:
            return "." * max_width
        else:
            return string[:max_width-3] + "..."
def conv_time(time):
    return f"[{int(time//60):02d}:{int(time % 60):02d}]"
#Versions of UI
def classic(stdscr, app_name: str, music_name: str, author: str, folder: str, options: list, time):
    height, width = stdscr.getmaxyx()
    stdscr.erase()
    y = 0
    stdscr.addstr(y, 0, cut_and_replace(app_name, width), curses.color_pair(1))
    stdscr.addstr(y+1, 0, cut_and_replace(music_name, width-10) + time, curses.color_pair(2))
    stdscr.addstr(y+2, 0, cut_and_replace(author, width), curses.color_pair(3))
    if not(configuration.UI_mode):
        stdscr.addstr(y+3, 0, cut_and_replace(folder, width), curses.color_pair(4))
    else:
        y -= 1
    stdscr.addstr(y + 4, 0, cut_and_replace(options, width), curses.color_pair(5))
    stdscr.addstr(y + 5, 0, cut_and_replace(instruction, width), curses.color_pair(5))
    stdscr.refresh()

def modern(stdscr, app_name: str, music_name: str, author: str, folder: str, options: str, time):
    height, width = stdscr.getmaxyx()
    stdscr.erase()
    y = 0
    stdscr.addstr(y, width//2-(len(str(app_name))//2), app_name, curses.color_pair(1))
    stdscr.addstr(y+1, 0, cut_and_replace(music_name, width//2 - 8), curses.color_pair(2))
    stdscr.addstr(y+1, width-8, time, curses.color_pair(2))
    stdscr.addstr(y+2, 0, cut_and_replace(author, width//2), curses.color_pair(3))
    if not(configuration.UI_mode):
        stdscr.addstr(y+3, 0, cut_and_replace(folder, width//2), curses.color_pair(4))
    else:
        y -= 1
    stdscr.addstr(y + 4, 0, cut_and_replace(options, width//2), curses.color_pair(5))
    stdscr.addstr(y + 5, 0, instruction, curses.color_pair(5))
    stdscr.refresh()

def minimal(stdscr, music_name: str, options):
    height, width = stdscr.getmaxyx()
    stdscr.erase()
    stdscr.addstr(0, 0, cut_and_replace(music_name[12:].strip(), width), curses.color_pair(2))
    stdscr.addstr(1, 0, options, curses.color_pair(5))
    stdscr.refresh()

def draw_information(stdscr, app_name: str, music_name: str, author: str, folder: str, options: list, player):
    global Minimal
    global instruction
    global UI_mode
    option_string = f"Status: stopped [{options[0]}], shuffled [{options[1]}]"


    height, width = stdscr.getmaxyx()
    if height <= Minimal[0] or width <= Minimal[1]:
        if UI_mode == "minimal":
            stdscr.clear()
            option_string = f"St[{str(options[0])[0]}],Sh[{str(options[1])[0]}]"
            minimal(stdscr, music_name, option_string)
            stdscr.refresh()
            return
        stdscr.clear()
        msg = "Too small window, expand it"
        stdscr.addstr(0,0, msg)
        stdscr.refresh()
        return 

    paramethers = (stdscr, app_name, music_name, author, folder, option_string, conv_time(player.curr_pos))
    if UI_mode == "classic":
        classic(*paramethers)

    elif UI_mode == "modern":
        modern(*paramethers)

    elif UI_mode == "minimal":
        option_string = f"St[{str(options[0])[0]}],Sh[{str(options[1])[0]}]"
        minimal(stdscr, music_name, option_string)
    