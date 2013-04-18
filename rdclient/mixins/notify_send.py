from rdclient import method
import subprocess


class NotifySendMixin(object):
    """Mixin for notify-send"""

    @method('None', summary='str', body='str')
    def notify_send(self, summary, body):
        """Send notification"""
        subprocess.call([
            'notify-send', summary, body,
        ])
