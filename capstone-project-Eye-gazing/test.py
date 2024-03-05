import numpy as np
import cv2

img = np.array([ 
    [[1, 2, 3], [2, 3, 1], [3, 1, 2]], 
    [[4, 5, 6], [65, 71, 72], [6, 4, 5]], 
    [[7, 8, 9], [8, 9, 7], [9, 7, 8]]], dtype=np.uint8)

lower = np.array([65, 71, 72])
upper = np.array([65, 71, 72])

mask = cv2.inRange(img, lower, upper)

masked = cv2.bitwise_and(img, img, mask=mask)

result = img - masked

print(result)
