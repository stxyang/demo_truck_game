from Display import Display
from Form import AppBar, Menu, MapForm, TrucksForm
from City import City
from Map import Map

class GameEngine:

    def __init__(self, display):
        
        self.display = display

        self.forms = []
        self.tabbar = AppBar(self)
        
    def initialize(self):
        self.cities = City.load()
        self._map = Map(self.cities)

        fm_map = MapForm(self)
        fm_trucks = TrucksForm(self)
        fm_menu = Menu(self)
        self.forms.append(fm_map)
        self.forms.append(fm_trucks)
        self.forms.append(fm_menu)

        self.current = 2
        self.focus = fm_menu.focus()

    def run(self):

        while True:
            #self.display.show()
            self.tabbar.show()
            self.forms[self.current].show()
            
            key_code = self.display.screen.getch()
            if self.focus.check_key(key_code):
                pass
            else:
                if ord('q') == key_code:
                    break

    def focus_to(self, new_focus):
        if self.focus:
            self.focus.defocus()
        
        if 'tabbar' == new_focus:
            self.focus = self.tabbar.focus()
        else:
            if 'map' == new_focus:
                self.current = 0

            self.focus = self.forms[self.current].focus()
        
