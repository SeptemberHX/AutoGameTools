from mss import mss
import numpy as np
import cv2
import os

from .logger import get_logger


MATCH_THRESHOLD = 0.95
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
    result = cv2.matchTemplate(src_image, target_image, cv2.TM_SQDIFF_NORMED)
    for r in result:
        if r.any() > MATCH_THRESHOLD:
            contain_flag = True
            break
    if contain_flag:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return min_loc[0], min_loc[1], target_image.shape[1] + min_loc[0], target_image.shape[0] + min_loc[1]
    else:
        return None


def check_contain_img(src_img, target_img):
    return get_matched_area(src_img, target_img) is not None


def get_resource_img(resource_dir_path, resource_name):
    img_path = os.path.join(resource_dir_path, resource_name)
    logger.info('read image ' + img_path)
    return cv2.imread(img_path)


if __name__ == '__main__':
    get_game_frame(0, 0, 3840, 2100)
