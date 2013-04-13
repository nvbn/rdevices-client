from rdclient import method
import subprocess


class RhythmboxMixin(object):
    """Mixin for rhythmbox"""

    @method('None', action='str')
    def action(self, action):
        """Execute action in smplayer"""
        subprocess.Popen([
            'smplayer', '-send-action', action,
        ])

    @method('None', path='str')
    def open(self, path):
        """Open file in smplayer"""
        subprocess.Popen([
            'smplayer', path,
        ])
