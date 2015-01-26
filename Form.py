import curses

class Form:
    def __init__(self, rows, cols):
        self.pad = curses.newpad(rows, cols)
#        self.pad.box()
        self.cols = cols
        self.rows = rows

        self.focused = False
        self.prev_form = None
        self.next_form = None

    def show(self):
        self.pad.refresh(0, 0, 4, 1, self.rows+4, self.cols+1)

    def check_key(self, key):

        if curses.KEY_UP == key:
            return self.on_arrow_key_pressed('UP')
        elif curses.KEY_DOWN == key:
            return self.on_arrow_key_pressed('DOWN')
        elif curses.KEY_LEFT == key:
            return self.on_arrow_key_pressed('LEFT')
        elif curses.KEY_RIGHT == key:
            return self.on_arrow_key_pressed('RIGHT')
        else:
            return False

    def on_arrow_key_pressed(self, direction):
        return True        




class Menu(Form):
    def __init__(self):
        Form.__init__(self, 27, 78)
        self.pad.box()
        self.item_width = 14
        self.item_height = 7
        self.items = []
        self.current = 0
        self.per_row = 4

        count = 0
        for key in [
            "Stats", "Events", "My Fleet", "Mission", 
            "Setting", "Logs", "BITBOOK", "Crew", 
            "4S Shop"]:
            item = self.pad.derwin(
                self.item_height,
                self.item_width,
                2 + (self.item_height+1) * (count/self.per_row),
                5 + (count % self.per_row) * (self.item_width+4)
            )
            item.border()
            item.addstr(3, 7-len(key)/2, key)
            
            self.items.append(item)
            count += 1

    def show(self):
        for i in range(len(self.items)):
            if self.current == i and self.focused:
                self.items[i].bkgd(curses.color_pair(1))
            else:
                self.items[i].bkgd(curses.color_pair(2))
            
        self.pad.refresh(0, 0, 4, 1, self.rows+4, self.cols+1)

    def on_arrow_key_pressed(self, direction):
        #button = self.items[self.current]
        row = self.current / self.per_row
        col = self.current % self.per_row

        if "UP" == direction:
            if row > 0:
                row -= 1
            else:
                return True

        elif "DOWN" == direction:
            row += 1
        elif "LEFT" == direction:
            if self.current > 0:
                col -= 1
        elif "RIGHT" == direction:
            col += 1
        
        new_pos = row * self.per_row + col
        if new_pos < 0:
            self.current = 0
        elif new_pos > len(self.items)-1:
            self.current = len(self.items)-1
        else:
            self.current = new_pos

        return False


class AppBar(Form):
    def __init__(self):
        Form.__init__(self, 3, 32)
        self.item_width = 10
        self.item_height = 3
        self.items = []
        self.current = 0

        count = 0
        for key in ["Map", "Trucks", "Menu"]:
            button = self.pad.derwin(
                self.item_height,
                self.item_width,
                0,
                (count % 3) * (self.item_width+1)
            )
            button.box()
            button.addstr(1, 5-len(key)/2, key)
            self.items.append(button)
            count += 1

    def show(self):
        for i in range(len(self.items)):
            if self.current == i and self.focused:
                self.items[i].bkgd(curses.color_pair(1))
            else:
                self.items[i].bkgd(curses.color_pair(2))

        self.pad.refresh(0, 0, 1, 47, 3, 80)

    def on_arrow_key_pressed(self, direction):

        new_pos = self.current

        if "UP" == direction:
            return False

        elif "DOWN" == direction:
            return True
        elif "LEFT" == direction:
            new_pos -= 1
        elif "RIGHT" == direction:
            new_pos += 1
        
        if new_pos < 0:
            self.current = 0
        elif new_pos > len(self.items)-1:
            self.current = len(self.items)-1
        else:
            self.current = new_pos

        return False

