#!/usr/bin/evn python3

import cv2
from auto_module import image


if __name__ == '__main__':
    announcement_close = image.get_gray_resource_img('./resources', 'home_mark.png')
    announcement = image.get_gray_resource_img('./test', 'test_home.png')

    result = image.get_matched_area(announcement, announcement_close)
    if result is not None:
        cv2.rectangle(announcement, (result[0], result[1]), (result[2], result[3]), (7, 249, 151), 2)

        cv2.imshow("announcement", announcement)
        # Press "q" to quit
        if cv2.waitKey(0) & 0xFF == ord("q"):
            cv2.destroyAllWindows()