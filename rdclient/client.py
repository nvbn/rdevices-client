from .base import Device
import socket
import json
import imp
import argparse
import sys
import os


class RDClient(object):
    """rdevic.es client"""

    def __init__(self, host_port, path):
        self._load(path)
        self._connect(host_port)
        self._declare_methods()
        self._create_device()

    def _load(self, path):
        """Import module with device"""
        imp.load_source('device_module', path)

    def _connect(self, host_port):
        """Connect to remote server"""
        self._sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM,
        )
        host, port = host_port.split(':')
        self._sock.connect((host, int(port)))

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
            char = self._sock.recv(1)
            if char == '\n':
                self._device.process_request(
                    json.loads(msg),
                )
                msg = ''
            else:
                msg += char


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('device', help='file with device declaration')
    parser.add_argument(
        '--server', '-s', default='localhost:8080',
        help='server host:port',
    )
    args = parser.parse_args(sys.argv[1:])
    client = RDClient(
        args.server,
        os.path.abspath(args.device),
    )
    client.run()

