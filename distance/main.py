import gc
import machine
import os
import time
from machine import Pin

gc.collect()

usec = 1/1000000

class PinMap(object):
    D0 = 16;
    D1 = 5;
    D2 = 4;
    D3 = 0;
    D4 = 2;
    D5 = 14;
    D6 = 12;
    D7 = 13;
    D8 = 15;
    D9 = 3;
    D10 = 1;

# class HCSR04:
#     """
#     Driver to use the untrasonic sensor HC-SR04.
#     The sensor range is between 2cm and 4m.
#     The timeouts received listening to echo pin are converted to OSError('Out of range')
#     """
#     # echo_timeout_us is based in chip range limit (400cm)
#     def __init__(self, pin, echo_timeout_us=500*2*30):
#         """
#         trigger_pin: Output pin to send pulses
#         echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
#         echo_timeout_us: Timeout in microseconds to listen to echo pin.
#         By default is based in sensor limit range (4m)
#         """
#         self.echo_timeout_us = echo_timeout_us
#         # Init trigger pin (out)
#         self.pin = machine.Pin(pin, mode=machine.Pin.OUT)
#         self.pin.value(0)

#     def _send_pulse_and_wait(self):
#         """
#         Send the pulse to trigger and listen on echo pin.
#         We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
#         """
#         self.pin.value(0) # Stabilize the sensor
#         time.sleep_us(5)
#         self.pin.value(1)

#         # Send a 10us pulse.
#         time.sleep_us(10)
#         self.pin.value(0)
#         self.pin.init(mode=machine.Pin.IN)
#         try:
#             pulse_time = machine.time_pulse_us(self.pin, 1, self.echo_timeout_us)
#             return pulse_time
#         except OSError as ex:
#             if ex.args[0] == 110: # 110 = ETIMEDOUT
#                 raise OSError('Out of range')
#             raise ex
#         finally:
#             self.pin.init(mode=machine.Pin.OUT)

#     def distance_mm(self):
#         """
#         Get the distance in milimeters without floating point operations.
#         """
#         pulse_time = self._send_pulse_and_wait()

#         # To calculate the distance we get the pulse_time and divide it by 2
#         # (the pulse walk the distance twice) and by 29.1 becasue
#         # the sound speed on air (343.2 m/s), that It's equivalent to
#         # 0.34320 mm/us that is 1mm each 2.91us
#         # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
#         mm = pulse_time * 100 // 582
#         return mm

#     def distance_cm(self):
#         """
#         Get the distance in centimeters with floating point operations.
#         It returns a float
#         """
#         pulse_time = self._send_pulse_and_wait()
#         print('[pulse]', pulse_time)

#         # To calculate the distance we get the pulse_time and divide it by 2
#         # (the pulse walk the distance twice) and by 29.1 becasue
#         # the sound speed on air (343.2 m/s), that It's equivalent to
#         # 0.034320 cm/us that is 1cm each 29.1us
#         cms = (pulse_time / 2) / 29.1
#         return cms

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin.
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms

led = machine.Pin(2, machine.Pin.OUT)
ultrasonic = HCSR04(PinMap.D2, PinMap.D3)

for x in range(10):
    distance = ultrasonic.distance_cm()
    print(distance)
    (led.on if distance > 10 else led.off)()
    time.sleep(.5)

# pin = machine.Pin(PinMap.D3, machine.Pin.OUT)
# pin.on()

# time.sleep(usec * 10)


