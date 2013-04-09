from rdclient import method
import subprocess


class RhythmboxMixin(object):
    """Mixin for rhythmbox"""

    def _call_rhythmbox(self, *args, **kwargs):
        """Call rhythmbox client"""
        return subprocess.Popen(
            ['rhythmbox-client'] + list(args),
            stdout=subprocess.PIPE,
            **kwargs
        )

    @method('None')
    def rhythmbox_quit(self):
        """Close rhythmbox"""
        self._call_rhythmbox('--quit')

    @method('None')
    def rhythmbox_next(self):
        """Next song"""
        self._call_rhythmbox('--next')

    @method('None')
    def rhythmbox_previous(self):
        """Previous song"""
        self._call_rhythmbox('--previous')

    @method('None')
    def rhythmbox_play(self):
        """Play"""
        self._call_rhythmbox('--play')

    @method('None')
    def rhythmbox_pause(self):
        """Pause"""
        self._call_rhythmbox('--pause')

    @method('None')
    def rhythmbox_play_pause(self):
        """Play/pause switch"""
        self._call_rhythmbox('--play-pause')

    @method('str')
    def rhythmbox_get_playing(self):
        """Get current song"""
        proc = self._call_rhythmbox('--print-playing')
        return proc.stdout.readline()

    @method('str', format='str')
    def rhythmbox_get_playing_format(self, format):
        """Get current song with format"""
        proc = self._call_rhythmbox('--print-playing-format', format)
        return proc.stdout.readline()
