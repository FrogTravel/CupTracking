import numpy as np
import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture('cup.ogv')


    while True:
        _, frame = cap.read()
        if frame is None:
            break

        cv2.imshow('feed', frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break

    cv2.destroyAllWindows()
