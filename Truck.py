
class Truck:

    @staticmethod
    def load():
        return [
            Truck('Easy Band', 'LT', 'Qingdao', 0),
            Truck('Quick Trans', 'LT', 'Qingdao', 0),
            Truck('BIG Mac', 'HT', 'Qingdao', 0)
        ]

    def __init__(self, name, model, loc, course):
        self.name = name
        self.model = model
        self.location = loc
        self.course = course
        self.route = []
        self.capacity = 3
        self.cargos = []

    def carry(self, cargo):
        
        if len(self.cargos) >= self.capacity:
            return False
        cargo.status = 'LOADED'        
        self.cargos.append(cargo)
        return True

    def dump(self, cargo):

        self.cargos.remove(cargo)
        
    def status(self):

        if 0 == self.course:
            if len(self.cargos) > 0:
                return "BOARDING"
            else:
                return "IDLE"
        else:
            return "ON THE WAY"
                
    def dest(self):

        if len(self.route) > 0:
            return self.route[-1]
        else:
            return self.location

    def in_city(self, city):
        if self.status() != "ON THE WAY":
            return self.location == city.name
        return False

    def add_course(self, city):
        self.route.append(city.name)
        self.course = 10

    def remove_course(self):
        self.location = self.route[0]
        self.route.remove(self.route[0])
        if len(self.route) > 0:
            self.course = 10
        
    def kick_off(self):
        if len(self.route) == 0:
            return
        #self.location = self.route[0]
        #self.route.remove(self.route[0])



        
