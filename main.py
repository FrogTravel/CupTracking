import numpy as np
import cv2

down_sample_factor = 10

if __name__ == '__main__':
    cap = cv2.VideoCapture('cup.ogv')

    while True:
        _, frame = cap.read()
        if frame is None:
            break

        frame_copy = frame.copy()
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        frame_copy = cv2.resize(frame_copy, (int(frame_copy.shape[1] / down_sample_factor),
                                int(frame_copy.shape[0] / down_sample_factor)))
        img_red, img_green, img_blue = cv2.split(frame_copy)

        for i in range(0, frame_copy.shape[0]):
            for j in range(0, frame_copy.shape[1]):
                if 20 < img_red[i, j] < 50 and \
                        40 < img_green[i, j] < 60 and \
                        60 < img_blue[i, j] < 255:
                    frame_copy[i, j] = 255
                else:
                    frame_copy[i, j] = 0

        cv2.imshow('Video', frame_copy)
        cv2.imshow('Blue', img_blue)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break

    cv2.destroyAllWindows()
