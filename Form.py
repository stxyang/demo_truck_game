import curses
import logging

class Form:
    def __init__(self, rows, cols):
        self.pad = curses.newpad(rows, cols)
#        self.pad.box()
        self.cols = cols
        self.rows = rows

        self._focus = False
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
        elif 10 == key:
            return self.on_enter_pressed()
        else:
            return False

    def focus(self):
        self._focus = True
        return self
    def defocus(self):
        self._focus = False
        return self
    def focused(self):
        return self._focus

    def on_arrow_key_pressed(self, direction):
        if "UP" == direction:
            self.ge.focus_to('tabbar')
        return True

    def on_enter_pressed(self):
        return True


class Menu(Form):
    def __init__(self, ge):
        Form.__init__(self, 27, 78)
        self.ge = ge
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
            if self.current == i and self.focused():
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
                self.ge.focus_to('tabbar')
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

        return True

class AppBar(Form):
    def __init__(self, ge):
        Form.__init__(self, 3, 32)
        self.ge = ge
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
            if self.current == i:
                if self.focused():
                    self.items[i].bkgd(curses.color_pair(1))
                else:
                    self.items[i].bkgd(curses.color_pair(3))
            else:
                self.items[i].bkgd(curses.color_pair(2))

        self.pad.refresh(0, 0, 1, 47, 3, 80)

    def on_arrow_key_pressed(self, direction):

        new_pos = self.current

        if "UP" == direction:
            return False
        elif "DOWN" == direction:
            self.ge.focus_to('')
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

        return True

    def on_enter_pressed(self):
        self.ge.cur_form = self.current
        self.ge.focus_to('')
        self.items[2].addstr(1, 3, "Exit")            

class MapForm(Form):

    def __init__(self, ge):
        Form.__init__(self, 27, 78)
        self.ge = ge
        self._map = ge._map
        self.pad.box()

        #self.pad.addch(4, 5, curses.ACS_DIAMOND)
        self.pad.hline(2, 6, 0, 20)
        self.pad.addch(2, 26, curses.ACS_URCORNER)
        self.pad.vline(3, 26, 0, 2)
        self.pad.addch(4, 26, curses.ACS_LLCORNER)
        self.pad.hline(4, 27, 0, 20)
        self.pad.addch(4, 46, curses.ACS_URCORNER)
        self.pad.vline(5, 46, 0, 4)
        self.pad.addch(9, 46, curses.ACS_LLCORNER)
        self.pad.hline(9, 47, 0, 27)
        self.pad.addch(9, 74, curses.ACS_URCORNER)
        self.pad.vline(10, 74, 0, 8)
        #self.pad.addch(9, 46, curses.ACS_DIAMOND)

        self.current = 0
        self.items = []
        counter = 0
        self.city_mapping = {}

        for city in sorted(self._map.get_visible_cities(), key=lambda c:-c.pos[0]):
            row, col = self._map.convert(city.pos)
            win = self.pad.derwin(2, 9, row-2, col-5)
            win.addch(1, 4, curses.ACS_DIAMOND)
            win.addstr(0, 4-len(city.name)/2, city.name)
            self.items.append(win)
            if city is self.ge.cur_city:
                self.current = counter
            self.city_mapping[counter] = city
            counter += 1

    def show(self):

        #self.pad.bkgd(curses.color_pair(1))
        for i in range(len(self.items)):
            win = self.items[i]
            if self.current == i:
                if self.focused():
                    win.bkgd(curses.color_pair(1))
                else:
                    win.bkgd(curses.color_pair(3))
            else:
                win.bkgd(curses.color_pair(2))

        self.pad.refresh(0, 0, 4, 1, self.rows+4, self.cols+1)

    def on_arrow_key_pressed(self, direction):
        
        if "UP" == direction:
            if self.current > 0:
                self.current -= 1
            else:
                self.ge.focus_to('tabbar')
                return True
        elif "DOWN" == direction:
            if self.current != len(self.items)-1:
                self.current += 1

        return True

    def on_enter_pressed(self):
        self.ge.cur_city = self.city_mapping[self.current]
        self.ge.focus_to('city')
        return True

class TrucksForm(Form):

    def __init__(self, ge):
        Form.__init__(self, 27, 78)
        self.ge = ge
        self.pad.box()

        self.items = []
        self.current = 0
        for i in range(5):
            item = self.pad.derwin(3, 72, 1+i*3, 3)
            item.box()
            item.addstr(1, 2, "Truck %d" % i)
            self.items.append(item)

    def show(self):

        for i in range(len(self.items)):
            if self.current == i:
                if self.focused():
                    self.items[i].bkgd(curses.color_pair(1))
                else:
                    self.items[i].bkgd(curses.color_pair(3))
            else:
                self.items[i].bkgd(curses.color_pair(2))

        self.pad.refresh(0, 0, 4, 1, self.rows+4, self.cols+1)

    def on_arrow_key_pressed(self, direction):
        
        if "UP" == direction:
            if self.current > 0:
                self.current -= 1
            else:
                self.ge.focus_to('tabbar')
                return True
        elif "DOWN" == direction:
            if self.current != len(self.items)-1:
                self.current += 1

        return False

class CityForm(Form):

    def __init__(self, ge):
        Form.__init__(self, 27, 78)
        self.ge = ge

        self.pad.box()

        self.placename = self.pad.derwin(5, 52, 4, 14)
        self.placename.box()

        win = self.pad.derwin(14, 5, 8, 18)
        win.box()
        win = self.pad.derwin(14, 5, 8, 57)
        win.box()

        self.pad.addch(8, 18, curses.ACS_TTEE)
        self.pad.addch(8, 22, curses.ACS_TTEE)
        self.pad.addch(8, 57, curses.ACS_TTEE)
        self.pad.addch(8, 61, curses.ACS_TTEE)

        #self.pad.addch(9, 46, curses.ACS_DIAMOND)

        self.buttons = []
        count = 0
        btn_height = 3
        btn_width = 10
        for key in ["Info", "Offers"]:
            button = self.pad.derwin(
                btn_height, btn_width,
                23, 2+(count % 3) * (btn_width + 1)
            )
            button.box()
            button.addstr(1, 5-len(key)/2, key)
            self.buttons.append(button)
            count += 1
                

    def show(self):
        
        self.placename.addstr(2, 1, ' ' * 50)
        self.placename.addstr(2, 26-len(self.ge.cur_city.name)/2, self.ge.cur_city.name)
        self.pad.refresh(0, 0, 4, 1, self.rows+4, self.cols+1)

    def on_arrow_key_pressed(self, direction):
        
        if "UP" == direction:
            self.ge.focus_to('tabbar')
            return True
        return True

    def on_enter_pressed(self):
        return True

   
