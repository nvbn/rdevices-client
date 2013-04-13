from rdclient import method
import subprocess


class SmplayerMixin(object):
    """Mixin for smplayer"""

    @method('None', action='str')
    def smplayer_action(self, action):
        """Execute action in smplayer"""
        subprocess.Popen([
            'smplayer', '-send-action', action,
        ])

    @method('None', path='str')
    def smplayer_open(self, path):
        """Open file in smplayer"""
        subprocess.Popen([
            'smplayer', path,
        ])
