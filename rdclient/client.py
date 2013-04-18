from .base import Device
import socket
import json
import imp
import argparse
import sys
import os
import time


class RDClient(object):
    """rdevic.es client"""

    def __init__(self, host_port, path):
        self._host_port = host_port
        self._load(path)
        self._connect()
        self._create_device()

    def _load(self, path):
        """Import module with device"""
        imp.load_source('device_module', path)

    def _create_connection(self):
        """Create connection to remote"""
        self._sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM,
        )
        host, port = self._host_port.split(':')
        self._sock.connect((host, int(port)))
        self._sock.settimeout(60)

    def _connect(self):
        """Connect to remote server"""
        while True:
            try:
                self._create_connection()
                self._declare_methods()
                break
            except socket.error:
                print 'Failed to connect'
                time.sleep(1)

    def _reconnect(self):
        """Reconnect"""
        self._sock.close()
        self._connect()

    def _declare_methods(self):
        """Declare device methods"""
        for declaration in Device.device.declarations():
            self.send(
                action='declare',
                **declaration
            )

    def _create_device(self):
        """Create device"""
        self._device = Device.device(self)

    def send(self, **data):
        """Send data to remote"""
        self._sock.send(
            json.dumps(data) + '\n',
        )

    def run(self):
        """Run client"""
        msg = ''
        while True:
            reconnect = False
            try:
                char = self._sock.recv(1)
                if char == '\n':
                    self._device.process_request(
                        json.loads(msg),
                    )
                    msg = ''
                else:
                    msg += char
                if not char:
                    reconnect = True
            except socket.timeout:
                reconnect = True
            if reconnect:
                self._reconnect()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('device', help='file with device declaration')
    parser.add_argument(
        '--server', '-s', default='conn.rdevic.es:9999',
        help='server host:port',
    )
    args = parser.parse_args(sys.argv[1:])
    client = RDClient(
        args.server,
        os.path.abspath(args.device),
    )
    client.run()


if __name__ == '__main__':
    main()

