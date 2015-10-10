import curses
from Form import Form

class List(Form):

    def __init__(self, ge, fields, items):
        Form.__init__(self, 27, 78)

        list_max_width = 76
        list_max_height = 4096
        self.view_point = 0
        self.win_list = curses.newpad(list_max_height, list_max_width)
        #self.win_list.box()
        self.ge = ge

        self.pad.box()
        self.items = []
        self.fields = fields
        self.list_items = []

        self.line_height = 3
        self.line_width = 72
        self.lines_per_page = 6
        self.current = 0

        self.header = self.pad.derwin(3, 72, 1, 3)
        #self.header.box()
        for field in self.fields:
            self.header.addstr(1, 2+field[0], field[1])
        self.pad.hline(3, 3, 0, 72)

        #self.update(items)

    def new_line(self, top, left):
        return self.win_list.derwin(self.line_height, self.line_width, top, left)

    def update(self):
        
        if len(self.list_items) > 0:
            for listitem in self.list_items:
                listitem.bkgd(curses.color_pair(2))
                listitem.clear()
                
        self.list_items = []
        if self.current > len(self.items)-1:
            self.current = 0
            self.view_point = 0

    def show(self):

        for i in range(len(self.list_items)):
            if self.current == i:
                if self.focused():
                    self.list_items[i].bkgd(curses.color_pair(1))
                else:
                    self.list_items[i].bkgd(curses.color_pair(3))
            else:
                self.list_items[i].bkgd(curses.color_pair(2))
    
        Form.show(self)
        self.win_list.refresh(self.view_point, 0, 8, 2, self.rows, self.cols)


    def on_arrow_key_pressed(self, direction):
        
        if "UP" == direction:
            if self.current > 0:
                self.current -= 1
            else:
                self.ge.focus_to('tabbar')
                return True
        elif "DOWN" == direction:
            if self.current < len(self.list_items)-1:
                self.current += 1
        
        self.view_point = self.current/self.lines_per_page * 3 * self.lines_per_page

        return False


class TruckList(List):

    def __init__(self, ge, trucks):

        List.__init__(self, ge, [
            [0, 'Name'],
            [15, 'Destination'],
            [32, 'Status']
        ], trucks)

    def update(self):
        List.update(self)
        self.items = self.ge.trucks

        for i in range(len(self.items)):
            listitem = self.new_line(i*3, 2)
            listitem.box()
            item = self.items[i]
            arr = [item.name, item.dest(), item.status()]

            for j in range(len(self.fields)):
                field = self.fields[j]
                listitem.addstr(1, 2+field[0], arr[j])
            self.list_items.append(listitem)

    def focus(self):
        Form.focus(self)

        self.update()
        return self

    def on_enter_pressed(self):
        truck = self.items[self.current]
        self.ge.cur_truck = truck
        if truck.status() == "ON THE WAY":
            self.ge.focus_to('wild')
        else:
            self.ge.move_to_city(truck.location)
            self.ge.focus_to('city')    

class CargoList(List):
    
    def __init__(self, ge, cargos):
        
        List.__init__(self, ge, [
            [0, 'Dest.'],
            [16, 'Item'],
            [40, 'Payment'],
            [54, 'Status']
        ], cargos)
        self.city = None
        self.truck = None
                      
    def update(self, city, truck):
        List.update(self)
        self.city, self.truck = (city, truck)
        self.items = self.city.cargos
        if self.truck is not None:
            self.items = sorted(self.items + self.truck.cargos, key=lambda c:(c.dest, c.name, c.uid))

	i = 0
        for i in range(len(self.items)):
            listitem = self.new_line(i*3, 2)
            listitem.box()
            item = self.items[i]
            arr = [item.dest, item.name, str(item.profit), item.status]

            for j in range(len(self.fields)):
                field = self.fields[j]
                listitem.addstr(1, 2+field[0], arr[j])
            self.list_items.append(listitem)

        if self.truck:
            button = self.new_line(i*3+3, 2)
            button.box()
            button.addstr(1, 10, 'GO')
            self.list_items.append(button)
            #button.clear()
            

    def focus(self):
        Form.focus(self)

        self.update(self.ge.cur_city, self.ge.cur_truck)
        return self

    def on_enter_pressed(self):
        if self.truck is None:
            return

        if self.current == len(self.items):
            self.ge.forms[0].mode = 'NAVI'
            self.ge.focus_to('map')
        else:
            cargo = self.items[self.current]
            if cargo.status == 'LOADED':
                if cargo.src == self.city.name:
                    cargo.status = ''
                else:
                    cargo.status = 'STACKED'
                self.city.add_cargos([cargo])
                self.truck.dump(cargo)
            elif cargo.status == 'STACKED' or cargo.status == '':
                if self.truck.carry(cargo):
                    self.city.remove_cargo(cargo)

        self.ge.focus_to('')
