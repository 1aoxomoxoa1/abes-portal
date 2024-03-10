import cv2
import numpy as np
from projected_keyboard_helper import *


class Keyboard:
    def __init__(self, width_keyboard, height_keyboard, offset_keyboard, initial_key='F'):
        self.width_keyboard = width_keyboard
        self.height_keyboard = height_keyboard
        self.offset_keyboard = offset_keyboard
        self.keys = self.get_keyboard()
        self.current_key = initial_key

    def get_keyboard(self):
        # Implement the get_keyboard function as you did before
        # ... (copy the function from your original code)
        """
        draw a keyboard qwerty 10 x 5

        returns a list that is an 2d array representing the 
        offset_keyboard = (int, int) is the spatial offset on x, y of the keyboard
        offset_keyboard used for balancing and fixing the keyboard to correct position
        """
        column = np.arange(0, self.width_keyboard, self.width_keyboard/ 10, dtype=int) + self.offset_keyboard[0]
        #np.arrange(start,stop,space between values,datatypr)
        row = np.arange(0, self.height_keyboard, self.height_keyboard/ 5, dtype=int) + self.offset_keyboard[1]

        box = int(self.width_keyboard / 10)

        color_board = (250, 0, 100)
        key_points = []
        # key_points.append([value, position of value in box,position of box in screen)
                        # key   center               upper-left                      bottom-right
        key_points.append(['1', (column[0], row[0]), (column[0]-box/2, row[0]-box/2), (column[0]+box/2, row[0]+box/2)])
        #key_points.append(['1', (column[0], row[0]), (column[0]-box/4, row[0]-box/4), (column[0]+box/4, row[0]+box/4)])
        key_points.append(['2', (column[1], row[0]), (column[1]-box/2, row[0]-box/2), (column[1]+box/2, row[0]+box/2)])
        key_points.append(['3', (column[2], row[0]), (column[2]-box/2, row[0]-box/2), (column[2]+box/2, row[0]+box/2)])
        key_points.append(['4', (column[3], row[0]), (column[3]-box/2, row[0]-box/2), (column[3]+box/2, row[0]+box/2)])
        key_points.append(['5', (column[4], row[0]), (column[4]-box/2, row[0]-box/2), (column[4]+box/2, row[0]+box/2)])
        key_points.append(['6', (column[5], row[0]), (column[5]-box/2, row[0]-box/2), (column[5]+box/2, row[0]+box/2)])
        key_points.append(['7', (column[6], row[0]), (column[6]-box/2, row[0]-box/2), (column[6]+box/2, row[0]+box/2)])
        key_points.append(['8', (column[7], row[0]), (column[7]-box/2, row[0]-box/2), (column[7]+box/2, row[0]+box/2)])
        key_points.append(['9', (column[8], row[0]), (column[8]-box/2, row[0]-box/2), (column[8]+box/2, row[0]+box/2)])
        key_points.append(['0', (column[9], row[0]), (column[9]-box/2, row[0]-box/2), (column[9]+box/2, row[0]+box/2)])

        key_points.append(['Q', (column[0], row[1]), (column[0]-box/2, row[1]-box/2), (column[0]+box/2, row[1]+box/2)])
        key_points.append(['W', (column[1], row[1]), (column[1]-box/2, row[1]-box/2), (column[1]+box/2, row[1]+box/2)])
        key_points.append(['E', (column[2], row[1]), (column[2]-box/2, row[1]-box/2), (column[2]+box/2, row[1]+box/2)])
        key_points.append(['R', (column[3], row[1]), (column[3]-box/2, row[1]-box/2), (column[3]+box/2, row[1]+box/2)])
        key_points.append(['T', (column[4], row[1]), (column[4]-box/2, row[1]-box/2), (column[4]+box/2, row[1]+box/2)])
        key_points.append(['Y', (column[5], row[1]), (column[5]-box/2, row[1]-box/2), (column[5]+box/2, row[1]+box/2)])
        key_points.append(['U', (column[6], row[1]), (column[6]-box/2, row[1]-box/2), (column[6]+box/2, row[1]+box/2)])
        key_points.append(['I', (column[7], row[1]), (column[7]-box/2, row[1]-box/2), (column[7]+box/2, row[1]+box/2)])
        key_points.append(['O', (column[8], row[1]), (column[8]-box/2, row[1]-box/2), (column[8]+box/2, row[1]+box/2)])
        key_points.append(['P', (column[9], row[1]), (column[9]-box/2, row[1]-box/2), (column[9]+box/2, row[1]+box/2)])

        key_points.append(['A', (column[0]+ box/3, row[2]), (column[0]+ box/3-box/2, row[2]-box/2), (column[0]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['S', (column[1]+ box/3, row[2]), (column[1]+ box/3-box/2, row[2]-box/2), (column[1]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['D', (column[2]+ box/3, row[2]), (column[2]+ box/3-box/2, row[2]-box/2), (column[2]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['F', (column[3]+ box/3, row[2]), (column[3]+ box/3-box/2, row[2]-box/2), (column[3]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['G', (column[4]+ box/3, row[2]), (column[4]+ box/3-box/2, row[2]-box/2), (column[4]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['H', (column[5]+ box/3, row[2]), (column[5]+ box/3-box/2, row[2]-box/2), (column[5]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['J', (column[6]+ box/3, row[2]), (column[6]+ box/3-box/2, row[2]-box/2), (column[6]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['K', (column[7]+ box/3, row[2]), (column[7]+ box/3-box/2, row[2]-box/2), (column[7]+ box/3+box/2, row[2]+box/2)])
        key_points.append(['L', (column[8]+ box/3, row[2]), (column[8]+ box/3-box/2, row[2]-box/2), (column[8]+ box/3+box/2, row[2]+box/2)])

        key_points.append(['Z', (column[0]+ box*2/3, row[3]), (column[0]+ box*2/3-box/2, row[3]-box/2), (column[0]+ box*2/3+box/2, row[3]+box/2)])
        key_points.append(['X', (column[1]+ box*2/3, row[3]), (column[1]+ box*2/3-box/2, row[3]-box/2), (column[1]+ box*2/3+box/2, row[3]+box/2)])
        key_points.append(['C', (column[2]+ box*2/3, row[3]), (column[2]+ box*2/3-box/2, row[3]-box/2), (column[2]+ box*2/3+box/2, row[3]+box/2)])
        key_points.append(['V', (column[3]+ box*2/3, row[3]), (column[3]+ box*2/3-box/2, row[3]-box/2), (column[3]+ box*2/3+box/2, row[3]+box/2)])
        key_points.append(['B', (column[4]+ box*2/3, row[3]), (column[4]+ box*2/3-box/2, row[3]-box/2), (column[4]+ box*2/3+box/2, row[3]+box/2)])
        key_points.append(['N', (column[5]+ box*2/3, row[3]), (column[5]+ box*2/3-box/2, row[3]-box/2), (column[5]+ box*2/3+box/2, row[3]+box/2)])
        key_points.append(['M', (column[6]+ box*2/3, row[3]), (column[6]+ box*2/3-box/2, row[3]-box/2), (column[6]+ box*2/3+box/2, row[3]+box/2)])

        key_points.append(['.', (column[8], row[3]), (column[8]-box/2, row[3]-box/2), (column[8]+box/2, row[3]+box/2)])
        key_points.append(["'", (column[9], row[3]), (column[9]-box/2, row[3]-box/2), (column[9]+box/2, row[3]+box/2)])

        key_points.append(['del', (column[0], row[4]), (column[0]-box/2, row[4]-box/2), (220, row[4]+box/3)])

        key_points.append(['##', (280,480), (220,430), (350,513)])
        key_points.append([' ', (column[4], row[4]), (column[3]-box/2, row[4]-box/2), (800, row[4]+box/2)])
        key_points.append(['?', (column[8], row[4]), (column[8]-box/2, row[4]-box/2), (column[8]+box/2, row[4]+box/2)])
        key_points.append(['!', (column[9], row[4]), (column[9]-box/2, row[4]-box/2), (column[9]+box/2, row[4]+box/2)])

        print(key_points)
        return key_points
    
    def get_next_key(self, direction):
        next_key = get_next_key_based_on_direction(self.current_key, direction)
        self.current_key = next_key

    

# -----   draw keyboard
def get_keyboard(width_keyboard , height_keyboard, offset_keyboard):
    """
    draw a keyboard qwerty 10 x 5

    returns a list that is an 2d array representing the 
    offset_keyboard = (int, int) is the spatial offset on x, y of the keyboard
    offset_keyboard used for balancing and fixing the keyboard to correct position
    """
    column = np.arange(0, width_keyboard, width_keyboard/ 10, dtype=int) + offset_keyboard[0]
    #np.arrange(start,stop,space between values,datatypr)
    row = np.arange(0, height_keyboard, height_keyboard/ 5, dtype=int) + offset_keyboard[1]

    box = int(width_keyboard / 10)

    color_board = (250, 0, 100)
    key_points = []
    # key_points.append([value, position of value in box,position of box in screen)
                    # key   center               upper-left                      bottom-right
    key_points.append(['1', (column[0], row[0]), (column[0]-box/2, row[0]-box/2), (column[0]+box/2, row[0]+box/2)])
    #key_points.append(['1', (column[0], row[0]), (column[0]-box/4, row[0]-box/4), (column[0]+box/4, row[0]+box/4)])
    key_points.append(['2', (column[1], row[0]), (column[1]-box/2, row[0]-box/2), (column[1]+box/2, row[0]+box/2)])
    key_points.append(['3', (column[2], row[0]), (column[2]-box/2, row[0]-box/2), (column[2]+box/2, row[0]+box/2)])
    key_points.append(['4', (column[3], row[0]), (column[3]-box/2, row[0]-box/2), (column[3]+box/2, row[0]+box/2)])
    key_points.append(['5', (column[4], row[0]), (column[4]-box/2, row[0]-box/2), (column[4]+box/2, row[0]+box/2)])
    key_points.append(['6', (column[5], row[0]), (column[5]-box/2, row[0]-box/2), (column[5]+box/2, row[0]+box/2)])
    key_points.append(['7', (column[6], row[0]), (column[6]-box/2, row[0]-box/2), (column[6]+box/2, row[0]+box/2)])
    key_points.append(['8', (column[7], row[0]), (column[7]-box/2, row[0]-box/2), (column[7]+box/2, row[0]+box/2)])
    key_points.append(['9', (column[8], row[0]), (column[8]-box/2, row[0]-box/2), (column[8]+box/2, row[0]+box/2)])
    key_points.append(['0', (column[9], row[0]), (column[9]-box/2, row[0]-box/2), (column[9]+box/2, row[0]+box/2)])

    key_points.append(['Q', (column[0], row[1]), (column[0]-box/2, row[1]-box/2), (column[0]+box/2, row[1]+box/2)])
    key_points.append(['W', (column[1], row[1]), (column[1]-box/2, row[1]-box/2), (column[1]+box/2, row[1]+box/2)])
    key_points.append(['E', (column[2], row[1]), (column[2]-box/2, row[1]-box/2), (column[2]+box/2, row[1]+box/2)])
    key_points.append(['R', (column[3], row[1]), (column[3]-box/2, row[1]-box/2), (column[3]+box/2, row[1]+box/2)])
    key_points.append(['T', (column[4], row[1]), (column[4]-box/2, row[1]-box/2), (column[4]+box/2, row[1]+box/2)])
    key_points.append(['Y', (column[5], row[1]), (column[5]-box/2, row[1]-box/2), (column[5]+box/2, row[1]+box/2)])
    key_points.append(['U', (column[6], row[1]), (column[6]-box/2, row[1]-box/2), (column[6]+box/2, row[1]+box/2)])
    key_points.append(['I', (column[7], row[1]), (column[7]-box/2, row[1]-box/2), (column[7]+box/2, row[1]+box/2)])
    key_points.append(['O', (column[8], row[1]), (column[8]-box/2, row[1]-box/2), (column[8]+box/2, row[1]+box/2)])
    key_points.append(['P', (column[9], row[1]), (column[9]-box/2, row[1]-box/2), (column[9]+box/2, row[1]+box/2)])

    key_points.append(['A', (column[0]+ box/3, row[2]), (column[0]+ box/3-box/2, row[2]-box/2), (column[0]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['S', (column[1]+ box/3, row[2]), (column[1]+ box/3-box/2, row[2]-box/2), (column[1]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['D', (column[2]+ box/3, row[2]), (column[2]+ box/3-box/2, row[2]-box/2), (column[2]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['F', (column[3]+ box/3, row[2]), (column[3]+ box/3-box/2, row[2]-box/2), (column[3]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['G', (column[4]+ box/3, row[2]), (column[4]+ box/3-box/2, row[2]-box/2), (column[4]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['H', (column[5]+ box/3, row[2]), (column[5]+ box/3-box/2, row[2]-box/2), (column[5]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['J', (column[6]+ box/3, row[2]), (column[6]+ box/3-box/2, row[2]-box/2), (column[6]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['K', (column[7]+ box/3, row[2]), (column[7]+ box/3-box/2, row[2]-box/2), (column[7]+ box/3+box/2, row[2]+box/2)])
    key_points.append(['L', (column[8]+ box/3, row[2]), (column[8]+ box/3-box/2, row[2]-box/2), (column[8]+ box/3+box/2, row[2]+box/2)])

    key_points.append(['Z', (column[0]+ box*2/3, row[3]), (column[0]+ box*2/3-box/2, row[3]-box/2), (column[0]+ box*2/3+box/2, row[3]+box/2)])
    key_points.append(['X', (column[1]+ box*2/3, row[3]), (column[1]+ box*2/3-box/2, row[3]-box/2), (column[1]+ box*2/3+box/2, row[3]+box/2)])
    key_points.append(['C', (column[2]+ box*2/3, row[3]), (column[2]+ box*2/3-box/2, row[3]-box/2), (column[2]+ box*2/3+box/2, row[3]+box/2)])
    key_points.append(['V', (column[3]+ box*2/3, row[3]), (column[3]+ box*2/3-box/2, row[3]-box/2), (column[3]+ box*2/3+box/2, row[3]+box/2)])
    key_points.append(['B', (column[4]+ box*2/3, row[3]), (column[4]+ box*2/3-box/2, row[3]-box/2), (column[4]+ box*2/3+box/2, row[3]+box/2)])
    key_points.append(['N', (column[5]+ box*2/3, row[3]), (column[5]+ box*2/3-box/2, row[3]-box/2), (column[5]+ box*2/3+box/2, row[3]+box/2)])
    key_points.append(['M', (column[6]+ box*2/3, row[3]), (column[6]+ box*2/3-box/2, row[3]-box/2), (column[6]+ box*2/3+box/2, row[3]+box/2)])

    key_points.append(['.', (column[8], row[3]), (column[8]-box/2, row[3]-box/2), (column[8]+box/2, row[3]+box/2)])
    key_points.append(["'", (column[9], row[3]), (column[9]-box/2, row[3]-box/2), (column[9]+box/2, row[3]+box/2)])

    key_points.append(['del', (column[0], row[4]), (column[0]-box/2, row[4]-box/2), (220, row[4]+box/3)])

    key_points.append(['##', (280,480), (220,430), (350,513)])
    key_points.append([' ', (column[4], row[4]), (column[3]-box/2, row[4]-box/2), (800, row[4]+box/2)])
    key_points.append(['?', (column[8], row[4]), (column[8]-box/2, row[4]-box/2), (column[8]+box/2, row[4]+box/2)])
    key_points.append(['!', (column[9], row[4]), (column[9]-box/2, row[4]-box/2), (column[9]+box/2, row[4]+box/2)])

    return key_points
# --------------------------------------------------
