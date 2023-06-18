import logging
import time
import threading
import RPi.GPIO as GPIO


class RelayChannel(threading.Thread):
    """Class to represent an individual relay channel"""

    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.pin = pin
        self.state = False
        self.previous_state = False
        logging.info(f'SETTING OUT FOR BCM {self.pin}')
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def test(self):
        logging.info(f"Testing BCM Pin #{self.pin}")
        sleep_time = 0.5
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(sleep_time)

    def run(self):
        while True:
            # Only do things if the current state doesn't equal the previous state
            if self.state != self.previous_state:
                if self.state:
                    GPIO.output(self.pin, GPIO.LOW)
                else:
                    GPIO.output(self.pin, GPIO.HIGH)
            self.previous_state = self.state
            time.sleep(0.001)

    def activate_relay(self):
        self.state = True

    def deactivate_relay(self):
        self.state = False


class RelayMasterController():
    """Class for controlling the relay"""

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.setup_channels()

    def __del__(self):
        GPIO.cleanup()

    def setup_channels(self):
        """Create a relayChannel class for each channel and start the tread - also maps pins for this particular install"""
        self.channels = {
            0: RelayChannel(24), # Pump
            1: RelayChannel(6), # Channels
            2: RelayChannel(13),
            3: RelayChannel(19),
            4: RelayChannel(26),
            5: RelayChannel(27),
            6: RelayChannel(17), # 16
            7: RelayChannel(16), #25
            8: RelayChannel(12),
            9: RelayChannel(20),
            10: RelayChannel(21),
            11: RelayChannel(5),
            12: RelayChannel(22),
        }
        for controller in self.channels.values():
            logging.info('Starting controller')
            controller.start()

    def system_tests(self):
        logging.info('Performing system tests')
        self.activate_pump()
        time.sleep(1)
        i = 0
        for controller in self.channels.values():
            print(controller)
            if i == 0:
                i = i + 1
                continue
            controller.activate_relay()
            time.sleep(0.3)
            controller.deactivate_relay()
            time.sleep(0.3)
            i = i + 1
        self.deactivate_pump()

    def activate_pump(self):
        logging.info('Activating pump')
        self.channels[0].activate_relay()

    def deactivate_pump(self):
        logging.info('Deactivating pump')
        self.channels[0].deactivate_relay()

    def activate_nozzel(self, nozzel_number):
        logging.info(f'Activating nozzel {nozzel_number}')
        if nozzel_number == 0:
            return
        self.channels[nozzel_number].activate_relay()

    def deactivate_nozzel(self, nozzel_number):
        logging.info(f'Deactivating nozzel {nozzel_number}')
        if nozzel_number == 0:
            return
        self.channels[nozzel_number].deactivate_relay()

    def open_all_nozzels(self):
        for x in list(self.channels.values())[2:]:
            x.activate_relay()

    def close_all_nozzels(self):
        for x in list(self.channels.values())[2:]:
            x.deactivate_relay()
