import numpy as np
import cv2

down_sample_factor = 8
tracking_path = []


# Bluring image to reduce noise
# Resizing so it will proceed faster
def preprocess(img):
    img_copy = img.copy()

    img_copy = cv2.GaussianBlur(img_copy, (15, 15), 0)
    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
    img_copy = cv2.resize(img_copy, (int(img_copy.shape[1] / down_sample_factor),
                                     int(img_copy.shape[0] / down_sample_factor)))

    return img_copy


# Color detection for light and dark blue color
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


# Erosion followed by dilation followed again by erosion gives not bad shape of a cup
def dilation_erosion(img):
    img_copy = img.copy()
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(img_copy, kernel, iterations=1)

    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations=10)

    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(dilation, kernel, iterations=2)

    return erosion


# Finding contours of the cup from thresholded image
def find_contours(img):
    img_copy = img.copy()
    th = 65 # Just because, magic number. Any number from 0 to 254 (I guess) will work
    _, img_bin = cv2.threshold(img_copy, th, 255, 0)

    contours, _ = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours


# I tried to implement intel logo tracking, but tired
def get_img_from_box(img, box):
    a, b, d, e, = box
    height = max(abs(a[1] - b[1]), abs(a[1] - d[1]), abs(a[1] - e[1]), abs(b[1] - d[1]), abs(d[1] - e[1]))
    width = max(abs(a[0] - b[0]), abs(a[0] - d[0]), abs(a[0] - e[0]), abs(b[0] - d[0]), abs(d[0] - e[0]))
    x = min(a[0], b[0], d[0], e[0])
    y = min(a[1], b[1], d[1], e[1])

    return img[y:y + height, x:x + width]


# Returns center from box from contours so it can be tracked
def get_center_from_box(box):
    a, b, d, e, = box
    height = max(abs(a[1] - b[1]), abs(a[1] - d[1]), abs(a[1] - e[1]), abs(b[1] - d[1]), abs(d[1] - e[1]))
    width = max(abs(a[0] - b[0]), abs(a[0] - d[0]), abs(a[0] - e[0]), abs(b[0] - d[0]), abs(d[0] - e[0]))
    x = min(a[0], b[0], d[0], e[0])
    y = min(a[1], b[1], d[1], e[1])

    return [x + int(width / 2), y + int(height / 2)]


if __name__ == '__main__':
    cap = cv2.VideoCapture('cup.ogv')
    is_on_video = False
    ap_counter = 0
    dis_counter = 0

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

        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY) # Need to work with find_contours method

        contours = find_contours(img_gray)

        for c in contours:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            width = rect[1][0]
            height = rect[1][1]
            if width > 50 and height > 50:
                cv2.drawContours(result_frame, [box], 0, (255, 255, 0), 3)

                tracking_path.append(get_center_from_box(box))

                if (len(tracking_path) > 1):
                    cv2.polylines(result_frame, np.int32([tracking_path]), 0, (255, 0, 255), 3)

                # Saving image if cup appeared on the screen
                if not is_on_video:
                    cv2.imwrite('/Users/ekaterina/PycharmProjects/testtaskmax/web/static/appeared/' + str(ap_counter) + '.png',
                                frame)
                    ap_counter += 1

                is_on_video = True

        # If not found and it is the first time -> saving an image
        if len(contours) == 0:  # not found
            if is_on_video:
                cv2.imwrite('/Users/ekaterina/PycharmProjects/testtaskmax/web/static/disappeared/' + str(dis_counter) + '.png',
                            frame)
                dis_counter += 1

            is_on_video = False

        cv2.imshow('Video', result_frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    cv2.destroyAllWindows()
