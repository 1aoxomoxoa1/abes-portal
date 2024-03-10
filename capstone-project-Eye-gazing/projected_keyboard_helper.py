import numpy as np

keyboard_orientation = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'None'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', "'", 'None'],
    ['del', '##', ' ', ' ', ' ', ' ', ' ', '?', '!', 'None']
]



direction_dict = {
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
    "UP": (-1, 0),
    "DOWN": (1, 0)
}

def get_next_key_based_on_direction(current_key, direction: str):
    if(direction == "STRAIGHT"): 
        return current_key
    
    a = np.array(keyboard_orientation, dtype=str)
    idx_current = np.where(a == current_key)
    idx_tuple = idx_current[0][0], idx_current[1][0]
    print(idx_tuple)
    result = idx_tuple[0] + direction_dict[direction][0], idx_tuple[1] + direction_dict[direction][1] 

    if(current_key == " "): 
        if(direction == "LEFT"):
            return '##'
        elif(direction == "RIGHT"):
            return '?'
        elif(direction == 'UP'):
            return 'B'
        else:
            return current_key

    next_key = None
    try:
        next_key = a[result[0]][result[1]]
    except Exception as e:
        next_key = None
        
    
    if(next_key != 'None' and next_key != None): 
        return next_key
    else: 
        return current_key


print(get_next_key_based_on_direction("N", "DOWN"))