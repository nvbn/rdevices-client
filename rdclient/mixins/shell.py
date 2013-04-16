from rdclient import method
import subprocess


class ShellMixin(object):
    """Mixin for shell"""

    @method('list', path='str')
    def shell_ls(self, path):
        """Do ls in shell"""
        proc = subprocess.Popen(['ls', path], stdout=subprocess.PIPE)
        return map(lambda line: line[:-1], proc.stdout.readlines())
