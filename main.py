import numpy as np
import cv2

down_sample_factor = 8


def preprocess(img):
    img_copy = img.copy()

    img_copy = cv2.GaussianBlur(img_copy, (15, 15), 0)
    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
    img_copy = cv2.resize(img_copy, (int(img_copy.shape[1] / down_sample_factor),
                                     int(img_copy.shape[0] / down_sample_factor)))

    return img_copy


def detect_blue_color(img):
    img_copy = img.copy()
    img_red, img_green, img_blue = cv2.split(img_copy)

    for i in range(0, img_copy.shape[0]):
        for j in range(0, img_copy.shape[1]):
            if (20 < img_red[i, j] < 50 and \
                32 < img_green[i, j] < 60 and \
                55 < img_blue[i, j] < 255) or \
                    (10 < img_red[i, j] < 27 and \
                     20 < img_green[i, j] < 33 and \
                     27 < img_blue[i, j] < 47):
                img_copy[i, j] = 255
            else:
                img_copy[i, j] = 0

    return img_copy


def dilation_erosion(img):
    img_copy = img.copy()
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(img_copy, kernel, iterations=1)

    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations=10)

    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(dilation, kernel, iterations=2)

    return erosion


def find_contours(img):
    img_copy = img.copy()
    th = 65
    _, img_bin = cv2.threshold(img_copy, th, 255, 0)

    contours, _ = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours


if __name__ == '__main__':
    cap = cv2.VideoCapture('cup.ogv')

    while True:
        _, frame = cap.read()
        if frame is None:
            break

        result_frame = frame.copy()

        frame_copy = preprocess(frame)

        img_blue_detected = detect_blue_color(frame_copy)

        img_preprocessed = dilation_erosion(img_blue_detected)

        img_resized = cv2.resize(img_preprocessed,
                                 (int(frame.shape[1]), int(frame.shape[0])))

        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)

        contours = find_contours(img_gray)

        for c in contours:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            width = rect[1][0]
            height = rect[1][1]
            if width > 50 and height > 50:
                cv2.drawContours(result_frame, [box], 0, (255, 255, 0), 3)

        cv2.imshow('Video', result_frame)
        cv2.imshow('Preproc', img_preprocessed)
        # cv2.imshow('Blue', img_blue_detected)
        # cv2.imshow('Dilation', img_preprocessed)
        # cv2.imshow('Scaled to orig', img_gray)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break

    cv2.destroyAllWindows()
