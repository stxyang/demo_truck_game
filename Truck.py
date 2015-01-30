
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
            return

        self.cargos.append(cargo)

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
