import random

class Cargo:

    @staticmethod
    def generate(city, cities, num):
    
        namelist = [
            "Apples", "Atom Clock", "Album", "Ancient Vases",
            "Bananas", "Bacon", "Beans", "Boat Parts",
            "Cabin", "CD Player", "Chairs", "Coal",
            "Desks", "Diamond", "Duck", "Documents"
        ]

        ret = []
        i = 0
        
        while True:
            if i >= num:
                break;
            dest_city = cities[random.randint(0, len(cities)-1)]
            if dest_city.name == city.name: 
                continue
            ret.append(Cargo(
                namelist[random.randint(0, len(namelist)-1)],
                city.name,
                dest_city.name
            ))
            i += 1

        return ret
        
    def __init__(self, name, src_city, dest_city):
        self.name = name
        self.src = src_city
        self.dest = dest_city
        self.status = ''
        self.profit = random.randint(1,5)*100
        self.uid = random.randint(3000000, 7999999)


    
