from rdclient import method
import subprocess


class OMXplayerMixin(object):
    """Mixin for omxplayer"""

    def _omxplayer_get_command(self):
        """Get command for run player"""
        return getattr(self.Meta, 'omxplayer', ['omxplayer'])

    def _omxplayer_check_runned(self):
        """Check payer is runned"""
        try:
            return self._omxplayer_instance.poll() is None
        except AttributeError:
            return False

    @method('None', key='str')
    def omxplayer_write(self, key):
        """
        Write to omxplayer stdin

        z           Show Info
        1           Increase Speed
        2           Decrease Speed
        j           Previous Audio stream
        k           Next Audio stream
        i           Previous Chapter
        o           Next Chapter
        n           Previous Subtitle stream
        m           Next Subtitle stream
        s           Toggle subtitles
        d           Subtitle delay -250 ms
        f           Subtitle delay +250 ms
        q           Exit OMXPlayer
        p           Pause/Resume
        -           Decrease Volume
        +           Increase Volume
        \x1B[D      Seek -30
        \x1B[C      Seek +30
        \x1B[B      Seek -600
        \x1B[A      Seek +600
        """
        if not self._omxplayer_check_runned():
            raise Exception('Not runned')
        self._omxplayer_instance.stdin.write(key)

    @method('None', path='str')
    def omxplayer_open(self, path):
        """Open omx player"""
        if self._omxplayer_check_runned():
            raise Exception('Already runned')
        self._omxplayer_instance = subprocess.Popen(
            self._omxplayer_get_command() + [path],
            stdin=subprocess.PIPE,
        )

    for method_name, key in (
        ('show_info', 'z'),
        ('increase_speed', '1'),
        ('decrease_speed', '2'),
        ('increase_speed', '1'),
        ('previous_audio_stream', 'j'),
        ('next_audio_stream', 'k'),
        ('previous_chapter', 'i'),
        ('next_chapter', 'o'),
        ('previous_subtitle_stream', 'n'),
        ('next_subtitle_stream', 'm'),
        ('toggle_subtitles', 's'),
        ('subtitle_delay_minus_250ms', 'd'),
        ('subtitle_delay_plus_250ms', 'f'),
        ('exit', 'q'),
        ('pause_resume', 'p'),
        ('decrease_volume', '-'),
        ('increase_volume', '+'),
        ('seek_minus_30ms', '\x1B[D'),
        ('seek_plus_30ms', '\x1B[C'),
        ('seek_minus_600ms', '\x1B[B'),
        ('seek_plus_600ms', '\x1B[A'),
    ):
        func_name = 'omxplayer_{}'.format(method_name)

        def temp_fnc(self, key=key):
            self.omxplayer_write(key)

        temp_fnc.func_name = func_name
        locals()[func_name] = method('None')(temp_fnc)
