from rdclient import Device, method


class Calc(Device):

    @method('int', x='int', y='int')
    def sum(self, x, y):
        return int(x) + int(y)

    @method('None', a='int')
    def do_nothing(self, a):
        pass

    class Meta:
        uuid = '69b4a97c-9402-11e2-abb0-5404a6499c84'
