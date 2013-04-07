from SimpleCV import *
from cv_run import shade_cards, get_grid, split_image
from cv_collect import base_path

tags = ["up", "down", "none"]

def train(tags):
    e = EdgeHistogramFeatureExtractor()
    hue = HueHistogramFeatureExtractor()
    morph = MorphologyFeatureExtractor()
    features = [e, hue, morph]
    c = MachineLearning.TreeClassifier(features)
    c.train([os.path.join(base_path, tag) for tag in tags], tags)
    return c

def test(c, tags):
    c.test([os.path.join(base_path, "test", tag) for tag in tags], tags)

def main(filename):
    c = train(tags)
    #test(c, tags)
    c.save(filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print """usage: python cv_train.py target_file"""
    else:
        main(sys.argv[1])
