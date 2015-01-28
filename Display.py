
import curses

from Form import AppBar

class Display:

    atom = False

    def __init__(self):
        if Display.atom:
            return None            
            
        self.screen = curses.initscr()
        

        self.windows = []
        self.frame = curses.newwin(32, 80)
        self.frame.keypad(1)
        self.frame.border()

        self.windows.append(self.frame)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(1)

        # Enable colorous output.
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.screen.bkgd(curses.color_pair(2))
 
        self.screen.refresh()

        Display.atom = True
        ## send no-delay here to accept command during tool running
        ## window.nodelay(1)

    def add_win(self):
        
        pass

    def show(self):
#        self.screen.refresh()
        for win in self.windows:
            win.refresh()

    def wait_anykey(self):
        self.screen.addstr(22, 12, "Press any key to exit ...")
        self.screen.nodelay(0)
        self.screen.getkey()

    def destroy(self):

        curses.nocbreak()
        curses.echo()
        curses.endwin()  # Terminate curses
        return False
