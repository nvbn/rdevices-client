from rdclient import method
import subprocess


class PactlMixin(object):
    """Mixin for pactl"""

    @method('None', sink='int', volume='str')
    def pactl_set_sink_volume(self, sink, volume):
        """Set sink volume"""
        subprocess.Popen([
            'pactl', '--', 'set-sink-volume', str(sink), str(volume),
        ])

    @method('None', source='int', volume='str')
    def pactl_set_source_volume(self, source, volume):
        """Set source volume"""
        subprocess.Popen([
            'pactl', '--', 'set-source-volume', str(source), str(volume),
        ])
