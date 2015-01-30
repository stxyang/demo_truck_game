import random

class Cargo:

    def __init__(self, name, src_city, dest_city):
        self.name = name
        self.src = src_city
        self.dest = dest_city
    

class CargoGenerator:
    
    namelist = [
        "Apples", "Atom Clock", "Album", "Ancient Vases",
        "Bananas", "Bacon", "Beans", "Boat Parts",
        "Cabin", "CD Player", "Chairs", "Coal",
        "Desks", "Diamond", "Duck", "Documents"
    ]

    @staticmethod
    def get_cargo(city, cities, num):
        ret = []
        i = 0
        
        while True:
            if i >= num:
                break;
            dest_city = cities[random.randint(0, len(cities)-1)]
            if dest_city.name == city.name: 
                continue
            ret.append(Cargo(
                CargoGenerator.namelist[random.randint(0, len(CargoGenerator.namelist)-1)],
                city.name,
                dest_city.name
            ))
            i += 1

        return ret
        

    
