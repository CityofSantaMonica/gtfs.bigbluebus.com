import os
import ssl
import sys
import time
import urllib2

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# take this job 10 seconds out of phase with the transfer from BBB
time.sleep(10)

agency = os.environ['swiftly_agency']
key = os.environ['swiftly_key']
url = 'https://api.goswift.ly/real-time/' + agency + '/gtfs-rt-trip-updates'
headers = {'Authorization': key}

print(agency)
print(sys.version)
print(url)

request = urllib2.Request(url=url,headers=headers)
response = urllib2.urlopen(request)

f = open("/home/site/wwwroot/tripupdates.bin", "wb")
content = response.read()
f.write(content)
f.close()