import sys
import os
import cv2
import numpy as np


KEY_UP = 0
KEY_DOWN = 1
KEY_LEFT = 2
KEY_RIGHT = 3

SIZE_INCREMENT = 20


def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


#
# change the perspective so that (hopefully) the sides of the book are parallel
#
def transform_image(image):
    SQUEEZE = 200
    # Locate points of the documents or object which you want to transform
    pts1 = np.float32([[0, 0], [1500, 0], [SQUEEZE, 4100], [1500-SQUEEZE, 4100]])
    pts2 = np.float32([[0, 0], [1500, 0], [0, 4100], [1500, 4100]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (1500, 4100))
    # Wrap the transformed image
    return(result)

def do_file(filename):

    img = cv2.imread("F-trimmed/" + filename, cv2.IMREAD_COLOR)

    img = transform_image(img)

    rect_left = 400
    rect_right = 1200
    rect_top = 100
    rect_bottom = 3400

    # white color in BGR
    color = (255, 255, 255)

    # Line thickness of 2 px
    thickness = 2

    chosen_index = -1
    while(True):
        top_left = (rect_left, rect_top)
        bottom_right = (rect_right, rect_bottom)
        tmp = img.copy()
        final_img = cv2.rectangle(tmp, top_left, bottom_right, color, thickness)
        cv2.imshow("work",final_img)
        c = cv2.waitKey(0)

        if c == ord('n'):
            cropped_img = img[rect_top:rect_bottom, rect_left:rect_right]
            cv2.imwrite("F/" + filename, cropped_img)
            return
        elif c == ord('q'):
            sys.exit(0)
        elif c == ord('r'):
            img = rotate_image(img, 15)
        elif c == ord(','):
            img = rotate_image(img, -1)
        elif c == ord('.'):
            img = rotate_image(img, 1)
        elif c == ord('2'):
            # move up
            rect_top += SIZE_INCREMENT
            rect_bottom += SIZE_INCREMENT
        elif c == ord('8'):
            # move down
            rect_top -= SIZE_INCREMENT
            rect_bottom -= SIZE_INCREMENT
        elif c == ord('4'):
            # move left
            rect_left -= SIZE_INCREMENT
            rect_right -= SIZE_INCREMENT
        elif c == ord('6'):
            # move right
            rect_left += SIZE_INCREMENT
            rect_right += SIZE_INCREMENT
        elif c == KEY_UP:
            # grow height
            rect_top -= SIZE_INCREMENT
            rect_bottom += SIZE_INCREMENT
        elif c == KEY_DOWN:
            # shrink height
            rect_top += SIZE_INCREMENT
            rect_bottom -= SIZE_INCREMENT
        elif c == KEY_LEFT:
            # shrink width
            rect_left += SIZE_INCREMENT
            rect_right -= SIZE_INCREMENT
        elif c == KEY_RIGHT:
            # grow width
            rect_left -= SIZE_INCREMENT
            rect_right += SIZE_INCREMENT
        else:
            print("Invalid input decimal %03d" % c)

def main():
    filenames_text = open(sys.argv[1]).read()
    filenames = filenames_text.split("\n")
    filenames = filenames[:-1]

    for f in filenames:
        print("f", f)
        do_file(f)



main()

