from rdclient import method
import serial


class ArduinoMixin(object):
    """Mixin for access arduino"""

    @property
    def arduino_serial(self):
        """Lazy create serial communication"""
        if not getattr(self, '_arduino_serial', None):
            try:
                tty = self.Meta.arduino_tty
            except AttributeError:
                raise Exception('Set up arduino_tty in device Meta')
            self._arduino_serial = serial.Serial(tty, 9600)
            self._arduino_serial.timeout = 3
        return self._arduino_serial

    def _arduino_reset(self):
        """Reset arduino and raise exception"""
        self._arduino_serial = None
        raise Exception('tty not open')

    @method('None', data='str')
    def arduino_write(self, data):
        """Write data to arduino tty"""
        try:
            self.arduino_serial.write(data)
        except serial.SerialException:
            self._arduino_reset()

    @method('str', bytes='int')
    def arduino_read_bytes(self, bytes):
        """Read bytes from arduino tty"""
        try:
            return self.arduino_serial.read(bytes)
        except serial.SerialException:
            self._arduino_reset()

    @method('str', symbol='int')
    def arduino_read_unitl(self, symbol):
        """Read until symbol from arduino tty"""
        try:
            data = ''
            while True:
                char = self.arduino_serial.read()
                data += char
                if char == symbol:
                    break
            return data
        except serial.SerialException:
            self._arduino_reset()

    @method('str')
    def arduino_read_line(self):
        """Read line from arduino tty"""
        try:
            return self.arduino_serial.readline()
        except serial.SerialException:
            self._arduino_reset()
