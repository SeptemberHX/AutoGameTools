# encoding: utf-8

import ctypes
import time

import numpy
import os

import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from mss import mss

from auto_module.logger import get_logger

MATCH_THRESHOLD = 0.9
logger = get_logger('image')


def get_game_frame(x, y, width, height):
    """
    Get one frame of the game with screenshot
    :param x: x position of left-top corner
    :param y: y position of left-top corner
    :param width: width of the active window
    :param height: height of the active window
    :return:
    """
    img = None
    with mss() as sct:
        img = np.array(sct.grab({"top": y, "left": x, "width": width, "height": height}))
        img = np.flip(img[:, :, :3], 2)
    return img


def get_matched_area(src_image, target_image):
    """
    Get the position of the target_image in the src_image,
      and return the area of the target image based on the size of the target image
    :param src_image: src image
    :param target_image: template
    :return: left, top, right, bottom
    """
    contain_flag = False
    result = cv2.matchTemplate(src_image, target_image, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= MATCH_THRESHOLD)
    # w, h = target_image.shape[::-1]
    w, h = target_image.shape[1], target_image.shape[0]
    for pt in zip(*loc[::-1]):
        contain_flag = True
    #     cv2.rectangle(src_image, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
    # if contain_flag:
    #     cv2.imshow('Detected', src_image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    if contain_flag:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return max_loc[0], max_loc[1], w + max_loc[0], h + max_loc[1]
    else:
        return None


def check_contain_img(src_img, target_img):
    return get_matched_area(src_img, target_img) is not None


def get_resource_img(resource_dir_path, resource_name):
    img_path = os.path.join(resource_dir_path, resource_name)
    # logger.info('read image ' + img_path)
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


class GameWindow:
    def __init__(self, game_title):
        ctypes.windll.user32.SetProcessDPIAware()
        self.game_title = game_title
        self.hwnd = win32gui.FindWindow(None, self.game_title)
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

    def game_screenshot(self):
        if not win32gui.IsIconic(self.hwnd):  # check whether the window is minize or not
            left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
            width = right - left
            height = bot - top

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(self.mfcDC, width, height)
            self.saveDC.SelectObject(saveBitMap)
            self.saveDC.BitBlt((0, 0), (width, height), self.mfcDC, (0, 0), win32con.SRCCOPY)
            signedIntsArray = saveBitMap.GetBitmapBits(True)
            im_opencv = numpy.fromstring(signedIntsArray, dtype='uint8')
            im_opencv.shape = (height, width, 4)
            # logger.info('screenshot shape: {0}'.format(im_opencv.shape))

            win32gui.DeleteObject(saveBitMap.GetHandle())
            return cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)

    def click(self, x, y):
        logger.info('offset: ({0}, {1})'.format(x, y))
        long_position = win32api.MAKELONG(x, y)
        back1 = win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        time.sleep(0.05)
        back2 = win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)