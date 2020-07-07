import os
import ssl
import sys
import time
import urllib2

def update(apisuffix, targetfile):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    agency = os.environ['swiftly_agency']
    key = os.environ['swiftly_key']
    url = 'https://api.goswift.ly/real-time/' + agency + '/' + apisuffix
    headers = {'Authorization': key}

    print(agency)
    print(sys.version)
    print(url)

    request = urllib2.Request(url=url,headers=headers)
    response = urllib2.urlopen(request)

    f = open("/home/site/wwwroot/" + targetfile, "wb")
    content = response.read()
    f.write(content)
    f.close()