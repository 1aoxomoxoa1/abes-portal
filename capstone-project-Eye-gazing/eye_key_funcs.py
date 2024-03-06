import cv2
import numpy as np
import random
import time
import dlib
import sys
import pyttsx3


print("\n\n" + sys.executable)
# voiceEngine = pyttsx3.init()
# newVoiceRate = 150
# newVolume = 1
# voiceEngine.setProperty('rate', newVoiceRate)
# voiceEngine.setProperty('volume', newVolume)
# # ------------------------------------ Inputs


#-----RECALIBRATE FOR ABE --------
RATIO_BLINKING = 0.23  # calibrate with my eyes
dict_color = {'green': (0, 255, 0),
              'blue': (255, 0, 0),
              'red': (0, 0, 255),
              'yellow': (0, 255, 255),
              'white': (255, 255, 255),
              'black': (0, 0, 0)}


# # ------------------------------------
# -----   Initialize camera
# Use cv2.VideoCapture() to get a video capture object for the camera.
# Set up an infinite while loop and use the read() method to read the frames using the above created object.
# Use cv2.imshow() method to show the frames in the video.
# Breaks the loop when the user clicks a specific key.
def init_camera(camera_ID):
    camera = cv2.VideoCapture(camera_ID)
    return camera


# --------------------------------------------------

# -----  black page [3 channels]
def make_black_page(size):
    page = (np.zeros((int(size[0]), int(size[1]), 3))).astype('uint8')
    return page


# --------------------------------------------------

# ----- Make white page [3 channels]
def make_white_page(size):
    page = (np.zeros((int(size[0]), int(size[1]), 3)) + 255).astype('uint8')
    return page


# --------------------------------------------------

# -----   Rotate / flip / everything else (NB: depends on camera conf)
def adjust_frame(frame):
    # frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = cv2.flip(frame, 1)
    return frame


# --------------------------------------------------

# ----- Shut camera / windows off
def shut_off(camera):
    camera.release()  # When everything done, release the capture
    cv2.destroyAllWindows()


# --------------------------------------------------

# ----- Show a window
def show_window(title_window, window):
    cv2.namedWindow(title_window)
    cv2.imshow(title_window, window)


# --------------------------------------------------

# ----- show on frame a box containing the face
def display_box_around_face(img, box, color, size):
    x_left, y_top, x_right, y_bottom = box[0], box[1], box[2], box[3]
    cv2.rectangle(img, (x_left - size[0], y_top - size[1]), (x_right + size[0], y_bottom + size[1]),
                  dict_color[color], 5)
    # cv2.rectangle(image, start_point, end_point, color, thickness)


# --------------------------------------------------

# ----- get mid point
def half_point(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


#the minor axis is vertical axis , top to bottom of eye
def get_minor_axis_idx(eye_coordinates):
    return (eye_coordinates[2][0] + eye_coordinates[3][0]) / 2 


def get_major_axis_idx(eye_coordinates):
    return (eye_coordinates[0][1] + eye_coordinates[1][1]) / 2 
# --------------------------------------------------

# ----- get coordinates eye
def get_eye_coordinates(landmarks, points):


    x_left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
    x_right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
    y_top = half_point(landmarks.part(points[1]), landmarks.part(points[2]))
    y_bottom = half_point(landmarks.part(points[5]), landmarks.part(points[4]))


    return x_left, x_right, y_top, y_bottom


# --------------------------------------------------

# ----- draw line on eyes
#------ img frame param CHANGES
def display_eye_lines(img, coordinates, color):
    cv2.line(img, coordinates[0], coordinates[1], dict_color[color], 2) #left side to right side
    cv2.line(img, coordinates[2], coordinates[3], dict_color["red"], 2) #top to bottom


# ----- this returns a frame with lines on the eyes, and leaves the img paramater unchanged
def return_display_eye_lines(img, coordinates, color):
    im_lines = img.copy()

    cv2.line(im_lines, coordinates[0], coordinates[1], dict_color[color], 2) #left side to right side
    cv2.line(im_lines, coordinates[2], coordinates[3], dict_color["red"], 2) #top to bottom

    return im_lines

# --------------------------------------------------

# ----- draw circle at face landmark points
def display_face_points(img, landmarks, points_to_draw, color):
    for point in range(points_to_draw[0], points_to_draw[1]):
        x = landmarks.part(point).x
        y = landmarks.part(point).y
        cv2.circle(img, (x, y), 4, dict_color[color], 2)


# --------------------------------------------------

# ----- function to check blinking
def is_blinking(eye_coordinates):
    blinking = False

    # print("eye coordinates")
    # print(eye_coordinates)

    major_axis = np.sqrt(
        (eye_coordinates[1][0] - eye_coordinates[0][0]) ** 2 + (eye_coordinates[1][1] - eye_coordinates[0][1]) ** 2)
    minor_axis = np.sqrt(
        (eye_coordinates[3][0] - eye_coordinates[2][0]) ** 2 + (eye_coordinates[3][1] - eye_coordinates[2][1]) ** 2)


    
    ratio = minor_axis / major_axis
    # print("major axis: ", major_axis)
    # print("minor axis: ", minor_axis)
    # print("ratio: ", ratio)

    if ratio < RATIO_BLINKING: blinking = True

    return blinking


# --------------------------------------------------
# ----- find the limits of frame-cut around the calibrated box
def find_cut_limits(calibration_cut, padding):
    x_cut_max = np.array(calibration_cut)
    x_cut_min = np.array(calibration_cut)
    y_cut_max = np.array(calibration_cut)
    y_cut_min = np.array(calibration_cut)

    x_cut_max1 = np.transpose(x_cut_max)
    x_cut_min1 = np.transpose(x_cut_min)
    y_cut_max1 = np.transpose(y_cut_max)
    y_cut_min1 = np.transpose(y_cut_min)

    #add padding so there is some pixels surrounding the cut for the eye
    x_cut_max2 = x_cut_max1[0].max() + padding
    x_cut_min2 = x_cut_min1[0].min() - padding
    y_cut_max2 = y_cut_max1[1].max() + padding
    y_cut_min2 = y_cut_min1[1].min() - padding
    
    # print("x_cut_min",x_cut_min)
    # print("x_cut_max",x_cut_max)
    # print("y_cut_min",y_cut_min)
    # print("y_cut_max",y_cut_max)

    # print("x_cut_min1", x_cut_min1)
    # print("x_cut_max1", x_cut_max1)
    # print("y_cut_min1", y_cut_min1)
    # print("y_cut_max1", y_cut_max1)

    # if(x_cut_min2 > x_cut_max2):
    #     x_cut_max2 =  -x_cut_min2
    # else:
    #     x_cut_min2 = -x_cut_max2

    # if(y_cut_min2 > y_cut_max2):
    #     y_cut_max2 = -y_cut_min2
    # else:
    #     y_cut_min2 = -y_cut_max2

    # print("x_cut_min2", x_cut_min2)
    # print("x_cut_max2", x_cut_max2)
    # print("y_cut_min2", y_cut_min2)
    # print("y_cut_max2", y_cut_max2)

    return x_cut_min2, x_cut_max2, y_cut_min2, y_cut_max2

# print(find_cut_limits([[170,289],[277,335],[409,292],[183,399]], 0))
# --------------------------------------------------
# ----- find if the pupil is in the calibrated frame
def pupil_on_cut_valid(pupil_on_cut, frame):
    in_frame_cut = False
    condition_x = ((pupil_on_cut[0] > 0) & (pupil_on_cut[0] < frame.shape[1]))
    condition_y = ((pupil_on_cut[1] > 0) & (pupil_on_cut[1] < frame.shape[0]))
    if condition_x and condition_y:
        in_frame_cut = True
    # print("cut fram.shape[0]", cut_frame.shape[0])
    # print("cut fram.shape[1]", cut_frame.shape[1])
    # print("result for pupil on cut valid",in_frame_cut)

    return in_frame_cut

#first frame we want to run this before we start finding the center of mass frame by frame
def get_calibrated_pupil_threshold(frame):
    #found through minimal testing 
    DOPE_RATIO_FOR_BW_BALACNCE = .06
    
    threshold = 30 #start w arbitrary num
    optimized = False
    while(not optimized): #run until good
        pass 



def get_pupil_dark_area(frame):
    # Convert the image from BGR to HSV color space
    # bgr = cv2.cvtColor(np.copy(frame), cv2.COLOR_GRAY2BGR)
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #so , on the grayscale, any pixel less than 30 will be assigned to 0 or pure blk
    threshold_value = 35  # Adjust as needed


    # a mask is the same size as our image, but has only two pixel
    # values, 0 and 255 -- pixels with a value of 0 (background) are
    # ignored in the original image while mask pixels with a value of
    # 255 (foreground) are allowed to be kept
    # Create a binary mask where pixels below the threshold are set to 255 (white) and others to 0 (black)
    _, binary_mask = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)

    # Apply the binary mask to the original image
    # result = cv2.bitwise_and(gray_image, gray_image, mask=binary_mask)

    # Create a binary result image
    result = np.zeros_like(gray_image)
    result[binary_mask > 0] = 255

    bw_ratio = np.count_nonzero(result == 0) / np.count_nonzero(result == 255)
    print(f'dope ratio : {bw_ratio}')

    # Define the lower and upper bounds of the color you want to identify
    #ref this link to try to get good HSV bounds 
    #https://web.cs.uni-paderborn.de/cgvb/colormaster/web/color-systems/hsv.html
    # sensitivity = 15
    # lower_white = np.array([0,0,255-sensitivity])
    # upper_white = np.array([255,sensitivity,255])

    # # Create a mask using inRange to threshold the image
    # mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # # Bitwise-AND the original image and the mask to get the result
    # result = cv2.bitwise_and(frame, frame, mask=mask)

    # result_frame = frame - result
    
    return result


#remember: the center of mass is derived from the MASS OF BLACK PIXELS
#the higher the threshold, the wider the striaght range will be 
def get_direction_from_center_of_mass(gray_scale_frame, center_mass_coords: tuple):
    threshold_factor = .2
    shape = gray_scale_frame.shape
    
    #get the middle for x and y of the frame
    center_frame_y = shape[0] / 2
    center_frame_x = shape[1] / 2

    print(f'center frame x = {center_frame_x}')
    print(f'center frame y = {center_frame_y}')

    x_threshold_straight = shape[1] * threshold_factor 
    y_threshold_straight = shape[0] * threshold_factor

    if(center_mass_coords[0] < center_frame_x - (x_threshold_straight * .5)):
        print("LEFT")
    elif(center_mass_coords[0] > center_frame_x + (x_threshold_straight * .5)):
        print("RIGHT")
    else: 
        print("STRAIGHT")



#this function will take the BW frame with the pupil and return the center of mass
def get_center_of_mass(gray_scale_frame):
    # Find indices where we have mass, the black pixels of the smaller frame
    mass_x, mass_y = np.where(gray_scale_frame == 0)
  
  
    # mass_x and mass_y are the list of x indices and y indices of mass pixels
    #NOTE: in image processing , x indexes represent the rows, or like the height of an image
    # y indexes will represent the columns, translating to the width of the image
    cent_x = np.average(mass_y)
    cent_y = np.average(mass_x)

    print('gray scale frame shape: ' , gray_scale_frame.shape)

    print(f'cent_x: {cent_x}')
    print(f'cent_y: {cent_y}')

    get_direction_from_center_of_mass(gray_scale_frame, (cent_x, cent_y))

    return cent_x, cent_y





#frame the pupil, step before we search for contrast to locate it within the eye
#frame: this is the OG frame 720 x 1280 
def frame_pupil(frame: np.ndarray, frame_w_eye_lines, eye_coordinates) -> np.ndarray:
    resize_eye_frame = 4.5 # scaling factor for window's size
    resize_frame = 0.3 # scaling factor for window's size
    end_frame_length = 250 #want final frame to be 250px

    x_cut_min, x_cut_max, y_cut_min, y_cut_max = find_cut_limits(eye_coordinates, 10)
    crop_pupil_frame = np.copy(frame[y_cut_min:y_cut_max, x_cut_min:x_cut_max, :])
    print('crop_pupil_frame shape: ', crop_pupil_frame.shape)
    pupil_bw_frame = get_pupil_dark_area(crop_pupil_frame)
    get_center_of_mass(pupil_bw_frame)

    # crop_frame = np.copy(frame[y_cut_min:y_cut_max, x_cut_min:x_cut_max, :])
    return pupil_bw_frame



# --------------------------------------------------

# ----- find projection on page
def project_on_page(img_from, img_to, point):
    scale = (np.array(img_to.shape) / np.array(img_from.shape))  # .astype('int')

    projected_point = (point * scale).astype('int')
    # print(projected_point)
    # print('####')

    return projected_point


# --------------------------------------------------

# -----   display keys on frame, frame by frame
def dysplay_keyboard(img, keys):
    color_board = (255, 250, 100)
    thickness1 = 4
    # i=50
    # j=100
    for key in keys:
        # print("key[0]",key[0])
        # print("key[1]",key[1])

        cv2.putText(img, key[0], (int(key[1][0]), int(key[1][1])), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 100),
                    thickness=3)
        # cv2.putText(img, (i,j), (i,j), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 100), thickness = 3)
        cv2.rectangle(img, (int(key[2][0]), int(key[2][1])), (int(key[3][0]), int(key[3][1])), color_board, thickness1)
        # cv2.rectangle(img, (i,j), (i,j), color_board, thickness1)


# ----------------------------str----------------------

# -----   check key on keyboard and take input
def identify_key(key_points, coordinate_X, coordinate_Y):
    pressed_key = False
    # print('coordinatex coordinatey',coordinate_X, coordinate_Y)
    for key in range(0, len(key_points)):
        condition_1 = np.mean(np.array([coordinate_Y, coordinate_X]) > np.array(key_points[key][2]))
        condition_2 = np.mean(np.array([coordinate_Y, coordinate_X]) < np.array(key_points[key][3]))

        if int(condition_1 + condition_2) == 2:
            pressed_key = key_points[key][0]
            break

    return pressed_key


# --------------------------------------------------

# -----   compute eye's radius
def take_radius_eye(eye_coordinates):
    radius = np.sqrt(
        (eye_coordinates[3][0] - eye_coordinates[2][0]) ** 2 + (eye_coordinates[3][1] - eye_coordinates[2][1]) ** 2)
    return int(radius)


# --------------------------------------------------
def talk(pressed_key):
    # if pressed_key == '.':
    #     voiceEngine.say('dot')
    #     voiceEngine.runAndWait()

    # elif pressed_key == '?':
    #     voiceEngine.say('questionmark')
    #     voiceEngine.runAndWait()
    # elif pressed_key == ' ':
    #     voiceEngine.say('space')
    #     voiceEngine.runAndWait()
    # elif pressed_key == '##':
    #     voiceEngine.say('newline')
    #     voiceEngine.runAndWait()
    # elif pressed_key == "'":
    #     voiceEngine.say('Apostrophe')
    #     voiceEngine.runAndWait()
    # elif pressed_key == "!":
    #     voiceEngine.say('Exclamationmark')
    #     voiceEngine.runAndWait()
    # elif pressed_key == "del":
    #     voiceEngine.say('delete')
    #     voiceEngine.runAndWait()
    # else:
    #     voiceEngine.say(pressed_key)
    #     voiceEngine.runAndWait()
    pass

def read_word(string):
    # r = ""
    # for i in string[::-1]:
    #     if i != " " and i!="#":
    #         r = r + i
    #     else:
    #         break
    # r = r[::-1]
    # print('r', r)
    # voiceEngine.say(r)
    # voiceEngine.runAndWait()
    pass
