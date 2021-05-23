import cv2 as cv
import numpy as np

from tracklib.algorithms import Camshift, Meanshift, OpticalFlow, TemplateMatching

class Tracker:
    def __init__(self, video, algorithm="MeanShift"):
        self.init_loc, frame = self.find_pink_glove(video)
        self.algorithm = self.choose_algorithm(algorithm, frame)

    def find_pink_glove(self, video):
        loc = None
        while loc is None:
            _, frame = video.read()
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            upper_range = np.array([359, 255, 255])
            lower_range = np.array([100, 100, 100])
            mask = cv.inRange(hsv, lower_range, upper_range)
            pink_contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

            if len(pink_contours) > 0:
                pink_area = max(pink_contours, key=cv.contourArea)
                loc = cv.boundingRect(pink_area)
        return loc, frame

    def update_init_loc(self, video):
        self.init_loc, frame = self.find_pink_glove(video)
        self.algorithm.update_view(frame, self.init_loc)

    def choose_algorithm(self, algorithm, frame):
        if algorithm == "MeanShift":
            return Meanshift(frame, self.init_loc)
        elif algorithm == "CamShift":
            return Camshift(frame, self.init_loc)
        elif algorithm == "OpticalFlow":
            return OpticalFlow(frame, self.init_loc)
        elif algorithm == "TemplateMatching":
            return TemplateMatching(frame, self.init_loc)
    
    def change_algorithm(self, algorithm, video, frame):
        self.update_init_loc(video)
        self.choose_algorithm(algorithm, frame)
