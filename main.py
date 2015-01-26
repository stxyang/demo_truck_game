
##
## This project is for prototype design of
## "Logistics" a trunk transportation game
##

## Game
## City
## Road
## 
## Truck
## Cargo

## Python's PEP8 style

## Please use Lucida Console for a correct table view

from Display import Display
from Form import AppBar, Menu

display = Display()

forms = []

app_bar = AppBar()
form_menu = Menu()
form_menu.focused = True

forms.append([app_bar, form_menu])
focus_control = form_current = form_menu

while True:
    display.show()
    app_bar.show()
    form_current.show()

    key_code = display.screen.getch()
    
    if focus_control.check_key(key_code):
        if focus_control == form_current:
            form_current.focused = False
            focus_control = app_bar
            app_bar.focused = True
        else:
            app_bar.focused = False
            focus_control = form_current
            form_current.focused = True


    if ord('q') == key_code:
        break
        
        

display.wait_anykey()
display.destroy()
