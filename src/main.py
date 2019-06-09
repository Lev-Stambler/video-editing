import numpy as np
import cv2

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 24, (1920,1080))

def overlay_image(l_img, s_img, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]
    l_img[y1:y2, x1:x2] = (s_img[:, :] +
                              l_img[y1:y2, x1:x2])
    return l_img


def rescale_frame(frame, factor):
    return cv2.resize(frame, (0, 0), fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)


def build_offset(smll_width, smll_height, lrg_width, lrg_height, padding=20):
    return [
        lrg_width - smll_width - padding,
        lrg_height - smll_height - padding
    ]


def build_video(cap_smll, cap_lrg):
    resize_factor = 0.2
    smll_width = int(cap_smll.get(3) * resize_factor)
    smll_height = int(cap_smll.get(4) * resize_factor)
    lrg_width = int(cap_lrg.get(3))
    lrg_height = int(cap_lrg.get(4))
    print(lrg_width, lrg_height)
    while(cap_smll.isOpened() and cap_lrg.isOpened()):
        ret, lrg_img = cap_smll.read()
        ret, smll_img = cap_lrg.read()
        if lrg_img is None or smll_img is None or ret is not True:
          break
        resized = rescale_frame(smll_img, resize_factor)
        offset = build_offset(smll_width, smll_height, lrg_width, lrg_height)
        overlayed = overlay_image(lrg_img, resized, *offset)
        # needs to be converted back to rgb
        out.write(overlayed)
        cv2.imshow('frame', overlayed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap_smll.release()
    cap_lrg.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    cap_smll = cv2.VideoCapture('../files/small.mp4')
    cap_lrg = cv2.VideoCapture('../files/large.mp4')
    build_video(cap_smll, cap_lrg)

main()
