import cv2
import time
import logging
import numpy as np


class PrinterController():
    """Module for controlling printer"""

    def __init__(self, pixel_width):
        """Instantiate the module"""
        self.pixel_width = pixel_width

    def print_line_to_console(self, line):
        line_string = ""
        for char in line:
            if char == 1:
                line_string = line_string + '#'
            else:
                line_string = line_string + ' '
        logging.info(line_string)

    def _convert_to_simple_array(self, array):
        """Iterates the pixel array and performs necessary actions"""
        simple_array = []
        if not array.shape[0] != self.pixel_width:
            array = np.rot90(array)
            array = np.flip(array)
        for pixel_line in array:
            simple_array.append([1 if x.all() else 0 for x in pixel_line])
        return simple_array
