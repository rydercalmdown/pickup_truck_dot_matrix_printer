import cv2
import numpy as np


class PixelConverter():
    """Module for converting text or an image into a binary pixel matrix"""

    def __init__(self, pixel_width):
        """Instantiate the class"""
        self.pixel_width = pixel_width
        self.font_stroke = 1
        self.border_modifier = 0.99

    def _make_image_greyscale(self, image):
        """Makes a colour image black and white"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _resize_image(self, image, preserve_aspect_ratio=True):
        """Resizes the image to the limits of the printer"""
        original_width = img.shape[1]
        original_height = img.shape[0]
        downscale_multiplier = float(self.pixel_width) / float(img.shape[1])
        if preserve_aspect_ratio:
            dimensions = [self.pixel_width, int(original_height * downscale_multiplier)]
        else:
            dimensions = [self.pixel_width, original_height]
        return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)

    def _make_image_black_white_binary(self, image):
        """Uses a threshold operation to convert the greyscale image to black-white"""
        _, bw_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return bw_image

    def convert_image_to_pixels(self, image):
        """Convert an image to pixels"""
        greyscale = self._make_image_greyscale(self._resize_image(image))
        black_white = self._make_image_black_white_binary(greyscale)

    def _create_blank_image(self, height):
        """Returns a blank RGB np array to the specified height and pixel width"""
        return np.zeros((self.pixel_width, height, 3), np.uint8)

    def _get_text_width_height(self, text):
        """Returns the width and height of the text with default font options"""
        width, height = cv2.getTextSize(text, self.font, self._get_font_scale(), self.font_stroke)[0]
        return width, height

    def _get_font_scale(self):
        """Returns the appropriate font scale"""
        return cv2.getFontScaleFromHeight(self.font, self.pixel_width - 2, self.font_stroke) * self.border_modifier

    def convert_text_to_pixels(self, text, font):
        """Converts ASCII text to pixels"""
        font = int(font)
        if font == 0:
            self.font = cv2.FONT_HERSHEY_PLAIN
        elif font == 1:
            self.font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        text_width, text_height = self._get_text_width_height(text)
        image = self._create_blank_image(text_width)
        colour = (255, 255, 255)
        max_lower = self.pixel_width
        position = (0, int(max_lower * self.border_modifier))
        cv2.putText(image, text, position, self.font, self._get_font_scale(), colour, self.font_stroke)
        return image
