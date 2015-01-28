
class Map:

    def __init__(self, cities):
        self.center = (565, 720)
        self.zoom = 4
        self.cities = cities
        
    def get_visible_cities(self):

        pos_top_left, pos_bottom_right = self.get_map_range()
        return filter(lambda x: x.pos < pos_bottom_right and x.pos > pos_top_left, self.cities)
            
    def get_map_range(self):
        # should relate to zoom
        center_lat, center_lng = self.center
        
        diff_y = self.zoom * 12
        diff_x = self.zoom * 12 * 2
        
        return (
            (center_lat-diff_y, center_lng-diff_x), 
            (center_lat+diff_y, center_lng+diff_x)
        )
        
    def convert(self, pos):
        lat, lng = pos
        center_lat, center_lng = self.center
        return (
            (center_lat-lat)*27/self.zoom/32+13,
            (lng-center_lng)*78/self.zoom/24+39
        )
            
