from Display import Display
from Form import AppBar, Menu, MapForm, TruckList, CityForm, CargoList
from City import City
from Map import Map
from Truck import Truck
from Cargo import Cargo

class GameEngine:

    def __init__(self, display):
        
        self.display = display

        self.forms = []
        self.tabbar = AppBar(self)
        
    def initialize(self):
        ## all cities
        self.cities = City.load()

        ## opend cities
        self.accessible_cities = self.cities
        for city in self.cities:
            city.add_cargos(Cargo.generate(city, self.cities, 5))

        ## owned trucks
        self.trucks = Truck.load()

        self.cur_city = self.cities[0]
        self.cur_truck = None
        self._map = Map(self.cities)

        fm_map = MapForm(self)
        fm_menu = Menu(self)
        fm_city = CityForm(self)
        fm_trucks = TruckList(self, [])
        fm_cargo = CargoList(self, [])
        self.forms.append(fm_map)
        self.forms.append(fm_trucks)
        self.forms.append(fm_menu)
        self.forms.append(fm_city)
        self.forms.append(fm_cargo)

        self.cur_form = 3
        self.focus = self.forms[self.cur_form].focus()

    def run(self):

        while True:
            #self.display.show()
            self.tabbar.show()
            self.forms[self.cur_form].show()
            
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
                self.cur_form = 0
            elif 'city' == new_focus:
                self.cur_form = 3
            elif 'cargolist' == new_focus:
                self.cur_form = 4

            self.focus = self.forms[self.cur_form].focus()
        
    def get_current_truck(self):

        for truck in self.trucks:
            if truck.status() == "ON THE WAY":
                continue
            if truck.location == self.cur_city.name:
                return truck
        return None

    def move_to_city(self, city_name):
        
        for city in self.cities:
            if city.name == city_name:
                self.cur_city = city
                break

            
