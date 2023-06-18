import os
import logging
import time
from flask import Flask, render_template, jsonify, request
from pixel_converter import PixelConverter
from printer_controller import PrinterController
from relay_controller import RelayMasterController


class MissionController():
    """Main class for controlling everything"""

    def __init__(self):
        self.set_up_flask()
        self.pixel_width = 12
        self.pixel_diameter = 4.5
        self.print_to_console = True
        self.pixel_converter = PixelConverter(self.pixel_width)
        self.printer_controller = PrinterController(self.pixel_width)
        self.relay_controller = RelayMasterController()
        self.relay_controller.system_tests()

    def _get_line_time_delay(self, speed_kph):
        """Returns the time delay for each line given the current speed in kph"""
        speed_cms = speed_kph * 100000 / 3600
        pixel_diameter_cm = self.pixel_diameter * 2.54
        pixels_per_second = speed_cms / pixel_diameter_cm
        delay = 1 / pixels_per_second
        return delay

    def _convert_text_to_array(self, text, font):
        """Converts the submitted text to a simple array"""
        logging.info('Converting text to array')
        img = self.pixel_converter.convert_text_to_pixels(text, font)
        return self.printer_controller._convert_to_simple_array(img)

    def iterate_array(self, simple_array, speed):
        """Iterates the simple array and makes the apporpriate downstream calls"""
        for line in simple_array:
            if self.print_to_console:
                self.printer_controller.print_line_to_console(line)
            # Activate Appropriate Relays if on raspberry pi
            for index, value in enumerate(line):
                if value == 1:
                    self.relay_controller.activate_nozzel(index)
                else:
                    self.relay_controller.deactivate_nozzel(index)
            time.sleep(self._get_line_time_delay(speed))

    def print_text(self, text, speed, font):
        logging.info(f'Speed - {speed} KPH')
        logging.info(f"Printing - '{text}'")
        simple_array = self._convert_text_to_array(text, font)
        self.relay_controller.activate_pump()
        time.sleep(2)
        self.iterate_array(simple_array, speed)
        time.sleep(2)
        self.relay_controller.deactivate_pump()

    def purge_system(self, seconds=3):
        logging.info('Purging system')
        self.relay_controller.open_all_nozzels()
        self.relay_controller.activate_pump()
        time.sleep(seconds)
        self.relay_controller.close_all_nozzels()
        self.relay_controller.deactivate_pump()
        logging.info('Purging complete')

    def set_up_flask(self):
        """Sets up the webserver """
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/print/', methods=['POST'])
        def endpoint_print_text():
            logging.info("Printing Request Received")
            text = request.form.get('text')
            speed = float(request.form.get('speed'))
            font = int(request.form.get('font'))
            print(f'font is {font}')
            self.print_text(text, speed, font)
            return jsonify({
                'status': 'ok',
            })

        @self.app.route('/on/', methods=['GET'])
        def turn_on():
            index = int(request.args.get('relay'))
            self.relay_controller.activate_nozzel(index)
            if index == 0:
                self.relay_controller.activate_pump()
            return jsonify({
                'status': 'ok',
            })

        @self.app.route('/off/', methods=['GET'])
        def turn_off():
            index = int(request.args.get('relay'))
            self.relay_controller.deactivate_nozzel(index)
            if index == 0:
                self.relay_controller.deactivate_pump()
            return jsonify({
                'status': 'ok',
            })

        @self.app.route('/purge/', methods=['POST'])
        def purge():
            logging.info("Purge Request Received")
            self.purge_system()
            return jsonify({
                'status': 'ok',
            })

    def run(self, host='0.0.0.0', port=8000):
        logging.info('Starting Flask')
        self.app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    mc = MissionController()
    mc.run()
