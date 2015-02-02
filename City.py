
class City:

    @staticmethod
    def load():
        return [
            City('Qingdao', 525, 740, 2),
            City('Jinan', 540, 710, 2),
            City('Beijing', 600, 700, 1),
            City('Guangzhou', 220, 630, 1),
            City('Tianjin', 590, 715, 1)
        ]

    def __init__(self, name, lat, lng, level):
        self.name = name
        self.pos = (lat, lng)
        self.level = level
        self.stack = []
        self.cargos = []
        self.trucks = []

        self.stack_limit = self.level * 5

    def add_cargos(self, cargos):
        self.cargos = sorted(self.cargos + cargos, key=lambda c:c.dest)

    def remove_cargo(self, cargo):
        self.cargos.remove(cargo)


