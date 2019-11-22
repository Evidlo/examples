# Evan Widloski - 2019-11-20
# Decoding remarkable xochitl.conf

from PyQt5.QtCore import QSettings

conf = QSettings('xochitl.conf', QSettings.IniFormat)

# read wifi settings for network 'test'
conf.value('wifinetworks/test')
# {'password': 'foobar00', 'protocol': 'psk', 'ssid': 'test'}

# set wifi settings
d = conf.value('wifinetworks/test')
d['password'] = 'baz'
conf.setValue('wifinetworks/test', d)
conf.sync()
