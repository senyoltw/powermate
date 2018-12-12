#mpd
from mpd import MPDClient

def connectMPD():
	try:
		client = MPDClient()               # create client object
		client.timeout = 200               # network timeout in seconds (floats allowed), default: None
		client.idletimeout = None
		#print "mpd Connecting..."
		client.connect("localhost", 6600)
		#print "mpd Connected!"
		return client
	except:
		print 'Could not connect to MPD server'

## powermate
import glob
from time import sleep
from powermate import PowerMateBase, LedEvent, MAX_BRIGHTNESS

class ExamplePowerMate(PowerMateBase):
  def __init__(self, path):
    super(ExamplePowerMate, self).__init__(path)
    self._pulsing = False
    self._brightness = MAX_BRIGHTNESS

  def short_press(self):
    print('Short press!')
    self._pulsing = not self._pulsing
    print(self._pulsing)

    if client.status()["state"] == "play":
      client.pause()
      print('Audio pause!')
    else:
      client.play()
      print('Audio play!')

    if self._pulsing:
      return LedEvent.pulse()
    else:
      return LedEvent(brightness=self._brightness)

  def long_press(self):
    print('Long press!')

  def rotate(self, rotation):
    #print('Rotate {}!'.format(rotation))
    self._brightness = max(0, min(MAX_BRIGHTNESS, self._brightness + rotation))
    self._pulsing = False

    cur_vol = int(client.status()["volume"])
    client.setvol(cur_vol + rotation)

    return LedEvent(brightness=self._brightness)

  def push_rotate(self, rotation):
    print('Push rotate {}!'.format(rotation))

    if rotation == 1:
      client.next()
    else:
      client.previous()
    sleep(0.5)

if __name__ == '__main__':
  client = connectMPD()
  pm = ExamplePowerMate(glob.glob('/dev/input/by-id/*PowerMate*')[0])
  pm.run()
  client.close()
