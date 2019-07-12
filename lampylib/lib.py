import abc
import logging
import re

import rtmidi


LOG = logging.getLogger()


class PortNotFound(Exception):

    def __init__(self, direction, port, ports):
        super().__init__(f"[{direction}] Port '{port}' is not found."
                         f"\n\tAvailable ports: {ports}")


class LPIO:

    MIDI_DEVICE = r".*Launchpad Mini.*"

    def open_midi_port(self, open_port):
        for port, name in enumerate(self.get_ports()):
            if re.match(self.MIDI_DEVICE, name):
                return open_port(port)
        else:
            raise PortNotFound("in" if isinstance(self, rtmidi.MidiIn) else "out",
                               self.MIDI_DEVICE, self.get_ports())


class LPMInChannel(rtmidi.MidiIn, LPIO):

    def open(self):
        return self.open_midi_port(self.open_port)


class LPMOutChannel(rtmidi.MidiOut, LPIO):

    def open(self):
        return self.open_midi_port(self.open_port)


class Button:

    @property
    def color(self):
        pass

    @color.setter
    def color(self, val):
        pass

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def special(self):
        return self.special # TODO ???

# TODO events, press release


class Launchpad:

    def __init__(self):
        self._in = None
        self._out = None

    def connect(self, port=None):
        self._in = LPMInChannel().open()
        self._out = LPMOutChannel().open()

        return self

    @property
    def input(self):
        return self._in

    @property
    def output(self):
        return self._out

    def get_button(self, x, y):
        raise NotImplementedError

    def clear(self, color=None):
        raise NotImplementedError

    def line(self, x, y, color):
        raise NotImplementedError

    def circle(self, x, y, r, color):
        raise NotImplementedError

    def rect(self, x, y, h, w, color):
        raise NotImplementedError

    def char(self, char, color):
        raise NotImplementedError

    def flash_string(self, string, color):
        raise NotImplementedError

    def scroll_string(self, string, color):
        raise NotImplementedError

    def draw_image(self, image):
        raise NotImplementedError

    # TODO Update
    def swap_buffers(self):
        raise NotImplementedError


class Command:

    TYPE_NOTE_ON = "note on"
    TYPE_NOTE_OFF = "note off"
    TYPE_CONTROLLER_CHANGE = "controller change"
    TYPE_UNKNOWN = "unknown"

    def __init__(self, msg_type, key, value, dt):
        self._type = msg_type
        self.key = key
        self.value = value
        self.dt = dt

    @property
    def type(self):
        return {
            0x80: self.TYPE_NOTE_OFF,
            0x90: self.TYPE_NOTE_ON,
            0xB0: self.TYPE_CONTROLLER_CHANGE,
        }.get(self._type, self.TYPE_UNKNOWN)

    @classmethod
    def from_message(cls, msg):
        payload, dt = msg
        msg_type, key, value = payload
        return cls(msg_type, key, value, dt)

    def as_message(self):
        return [self.type, self.key, self.value]

    def __str__(self):
        return "IN: type = {0}, kv = {1}:{2}, dt = {3}".format(
            self.type, self.key, self.value, self.dt)


class LEDMode:

    def __init__(self, color):
        self.color = color

    @property
    def low(self):
        return "low"

    @property
    def medium(self):
        return "medium"

    @property
    def high(self):
        return "high"


class Color:

    def __init__(self, r, g):
        self.r = str(bin(r))[2:]
        self.g = str(bin(g))[2:]
        self.copy = "0"
        self.clear = "0"

    @property
    def red(self):
        return LEDMode("red")

    @property
    def green(self):
        return LEDMode("green")

    @property
    def yellow(self):
        return LEDMode("yellow")

    @property
    def orange(self):
        return LEDMode("orange")

    def as_binary(self):
        return int("0b{r}{copy}{clear}{g}0".format(**self.__dict__), 2)
