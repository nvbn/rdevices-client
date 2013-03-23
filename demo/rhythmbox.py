from rdclient import Device, method
import os
import commands


class Rhythmbox(Device):
    @method("None")
    def next_song(self):
        """Run next song"""
        os.system('rhythmbox-client --next')

    @method("None")
    def prev_song(self):
        os.system('rhythmbox-client --previous')

    @method('str')
    def now(self):
        return commands.getoutput('rhythmbox-client --print-playing')

    class Meta:
        uuid = 'c841b6bc-9400-11e2-bb09-5404a6499c84'

