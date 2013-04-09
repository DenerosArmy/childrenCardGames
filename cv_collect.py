from SimpleCV import *
import sys
import os, os.path
import time
from cv_run import shade_cards, get_grid, split_image

base_path = "/home/nikita/Desktop/classifier"

def save_training(images, tag):
    if not os.path.exists(os.path.join(base_path, tag)):
        if tag.startswith("test/") and not os.path.exists(os.path.join(base_path, "test")):
            os.mkdir(os.path.join(base_path, "test"))
        os.mkdir(os.path.join(base_path, tag))
    n = 0
    for row in images:
        for img in row:
            img.save(os.path.join(base_path, tag, "{}-{}.png".format(int(time.time()), n)))
            n += 1


def main(tag):
    disp = Display((640, 360), title="Collect")
    top_row = []
    bottom_row = []
    blobs = []
    img = None
    while disp.isNotDone():
        if disp.mouseRight:
            img = cam.getImage().scale(640, 360)
        elif disp.mouseMiddle and img is not None:
            try:
                top_row, bottom_row, blobs = get_grid(img)
            except IndexError:
                img.dl().rectangle([0, 0], [640, 360], color=Color.RED, filled=True, alpha=150)
        elif disp.mouseLeft and img is not None:
            images = split_image(img, top_row, bottom_row)
            save_training(images, tag)
            img.dl().rectangle([0, 0], [640, 360], color=Color.BLACK, filled=True, alpha=200)
            img.save(disp)
            img = None

        if img is not None:
            shade_cards(img, top_row, bottom_row, 90)
            img.save(disp)
            img.clearLayers()
    disp.quit()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print """usage: python cv_collect.py tag"""
    else:
        # TODO: camera start is buggy because the index changes
        cam = Camera(2)
        main(sys.argv[1])
