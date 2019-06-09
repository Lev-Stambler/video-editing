import numpy as np
import cv2


def overlay_image(l_img, s_img, x_offset, y_offset):
    # add alphas
    l_img = cv2.cvtColor(l_img, cv2.COLOR_RGB2RGBA)
    s_img = cv2.cvtColor(s_img, cv2.COLOR_RGB2RGBA)

    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]
    alpha_s = s_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    for c in range(0, 3):
        l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                  alpha_l * l_img[y1:y2, x1:x2, c])

def rescaleFrame(frame, factor):
    return cv2.resize(frame, (0, 0), fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)


def main():
    cap = cv2.VideoCapture('../files/small.mp4')
    cap2 = cv2.VideoCapture('../files/large.mp4')

    while(cap.isOpened() or cap2.isOpened()):
        ret, frame = cap.read()
        ret, frame2 = cap2.read()
        resized = rescaleFrame(frame, 0.9)
        overlayed = overlay_image(frame, resized, 50, 50)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
