from SimpleCV import *
import requests

post_url = "http://pythonscript.denerosarmy.com:8000/cv"


def shade_cards(img, top_row, bottom_row, radius=50):
    for i, pt in enumerate(top_row):
        img.dl().centeredRectangle(pt, [radius, radius], Color.BLUE)
    for i, pt in enumerate(bottom_row):
        img.dl().centeredRectangle(pt, [radius, radius], Color.BLUE)

def get_grid(img):
    _, cr, _ = img.toYCrCb().splitChannels()
    blobs = cr.binarize(150).dilate(12).invert().findBlobs()
    for blob in blobs:
        x, y = blob.centroid()
        img.dl().circle((int(x), int(y)), 15, color=Color.WHITE, width=3)
    if len(blobs) != 4:
        raise IndexError, "wrong number of blobs"
    centroids = [blob.centroid() for blob in blobs]
    centroids.sort()
    left = (centroids[0][0] + centroids[1][0]) / 2
    right = (centroids[2][0] + centroids[3][0]) / 2
    centroids.sort(key=lambda pt: pt[1])
    top = (centroids[0][1] + centroids[1][1]) / 2
    bottom = (centroids[2][1] + centroids[3][1]) / 2
    
    coords = np.array(range(6+1)) / 6.0 * (right - left) + left
    top_row = [[0, 0] for _ in range(6+1)]
    bottom_row = [[0, 0] for _ in range(6+1)]
    for i in range(6+1):
        top_row[i][0] = coords[i]
        bottom_row[i][0] = coords[i]
        top_row[i][1] = top
        bottom_row[i][1] = bottom
    return top_row, bottom_row, blobs

def split_image(img, top_row, bottom_row):
    images = [[None for _ in top_row] for _ in range(2)]
    for i, pt in enumerate(top_row):
        images[0][i] = img.crop(pt[0], pt[1], 90, 90, centered=True)
    for i, pt in enumerate(bottom_row):
        images[1][i] = img.crop(pt[0], pt[1], 90, 90, centered=True)
    return images

def classify_split(c, images):
    classes = [["none" for _ in images[0]] for _ in images]
    for x, row in enumerate(images):
        for y, img in enumerate(rows):
            classes[x][y] = c

def notify_class_changed(x, y, old, new):
    print "Detected class change at ({}, {}) from '{}' to '{}'".format(x, y, old, new)
    d = {
            "position": y + x * 7,
            "old": old,
            "new": new
        }
    try:
        requests.post(post_url, d)
    except requests.RequestException as e:
        print "Caught exception", e

def main():
    disp = Display((640, 360), title="Run")
    top_row = []
    bottom_row = []
    blobs = []
    img_prev = cam.getImage().scale(640, 360)
    x, y = 0, 0
    classes = [["none" for _ in range(7)] for _ in range(2)]
    timer = 0
    while disp.isNotDone():
        img = cam.getImage().scale(640, 360)
        if disp.mouseRight:
            disp.quit()
            break
        elif disp.mouseLeft:
            try:
                top_row, bottom_row, blobs = get_grid(img)
            except IndexError:
                img.dl().rectangle([0, 0], [640, 360], color=Color.RED, filled=True, alpha=150)

        motion = (img - img_prev).binarize(30).histogram(2)[0]
        if motion > 50:
            timer = 7

        if timer > 0:
            img.dl().rectangle([0, 0], [640, 360], color=Color.BLACK, filled=True, alpha=100)
        else:
            if (x == 0 and y < len(top_row)) or (x == 1 and y < len(bottom_row)):
                if x == 0:
                    row = top_row
                else:
                    row = bottom_row
                pt = row[y]
                cropped = img.crop(pt[0], pt[1], 90, 90, centered=True)
                new = c.classify(cropped)
                if classes[x][y] != new:
                    notify_class_changed(x, y, classes[x][y], new)
                    classes[x][y] = new
                y = (y + 1) % 7
                if y == 0:
                    x = (x + 1) % 2

        for i, pt in enumerate(top_row):
            img.dl().text(classes[0][i], pt, color=(178,75,255))
        for i, pt in enumerate(bottom_row):
            img.dl().text(classes[1][i], pt, color=(178,75,255))
        timer = max(timer - 1, 0)
        shade_cards(img, top_row, bottom_row, 90)
        img.save(disp)
        img_prev = img
        img_prev.clearLayers()
    disp.quit()

if __name__ == '__main__':
    c = SimpleCV.TreeClassifier.load("classifier-11-20")
    # TODO: camera start is buggy because the index changes
    cam = Camera(2)

    main()


