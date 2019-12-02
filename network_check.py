import config
import urllib2
print("Checking network status...")
def internet_on():
	try:
		urllib2.urlopen(config.SERVER_IP, timeout=1)
		config.wifi=True
		print("Wifi available")
		return True
	except urllib2.URLError as err:
		config.wifi=False
		return False
