import threading

from Display import Display
from Form import AppBar, StatusBar, Menu, MapForm, CityForm, WildForm
from List import TruckList, CargoList
from City import City
from Map import Map
from Truck import Truck
from Cargo import Cargo

class GameEngine:

    def __init__(self, display):
        
        self.display = display

        self.forms = []
        self.statusbar = StatusBar(self)
        self.tabbar = AppBar(self)
        self.fund = 0
        self.status = ''
#        self.refresh_lock = threading.Lock()
        
    def initialize(self):
        self.status = 'INIT'
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
        fm_trucks = TruckList(self, [])
        fm_menu = Menu(self)
        fm_city = CityForm(self)
        fm_cargo = CargoList(self, [])
        fm_wild = WildForm(self)

        self.forms.append(fm_map)
        self.forms.append(fm_trucks)
        self.forms.append(fm_menu)
        self.forms.append(fm_city)
        self.forms.append(fm_cargo)
        self.forms.append(fm_wild)

        self.cur_form = 3
        self.focus = self.forms[self.cur_form].focus()

        self.refresh_truck()

    def run(self):
        self.status = 'RUNNING'

        while True:
            self.refresh()

            key_code = self.display.screen.getch()
            if self.focus.check_key(key_code):
                pass
            else:
                if ord('q') == key_code:
                    self.status = 'TEARDOWN'
                    break

    def refresh(self):
#        if not self.refresh_lock.acquire(False):
#            return
        #self.display.show()
        self.statusbar.show()
        self.tabbar.show()
        self.forms[self.cur_form].show()
#        self.refresh_lock.release()

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
            elif 'wild' == new_focus:
                self.cur_form = 5

            self.focus = self.forms[self.cur_form].focus()
        
    def get_current_truck(self):

        for truck in self.trucks:
            if truck.status() == "ON THE WAY":
                continue
            if truck.location == self.cur_city.name:
                return truck
        return None

    def get_city_by_name(self, city_name):
        for city in self.cities:
            if city.name == city_name:
                return city
        return None

    def move_to_city(self, city_name):
        self.cur_city = self.get_city_by_name(city_name)

    def truck_arrived(self, truck):
        
        arrived_cargos = []
        for cargo in truck.cargos:
            if cargo.dest == truck.location:
                arrived_cargos.append(cargo)
                self.fund += cargo.profit

        for cargo in arrived_cargos:
            truck.dump(cargo)

    def refresh_truck(self):
        for truck in self.trucks:
            if truck.course > 0:
                truck.course -= 1
                if truck.course == 0:
                    truck.remove_course()
                    self.truck_arrived(truck)
                    if (truck == self.cur_truck and\
                        (self.cur_form == 5 or self.cur_form == 3)) or\
                        self.cur_form == 1:
                        self.focus_to('')
                        self.refresh()
                else:
                    if truck == self.cur_truck and self.cur_form == 5:
                        self.focus_to('')
                        self.refresh()

        if self.status != 'TEARDOWN':
            threading.Timer(1, self.refresh_truck).start()
