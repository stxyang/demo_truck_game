
class City:

    @staticmethod
    def load():
        return [
            City('Qindao', 525, 740, 2),
            City('Jinan', 540, 710, 2),
            City('Beijing', 600, 700, 1),
            City('Guangzhou', 220, 630, 1),
            City('Tianjin', 595, 715, 1)
        ]

    def __init__(self, name, lat, lng, level):
        self.name = name
        self.pos = (lat, lng)
        self.level = level
