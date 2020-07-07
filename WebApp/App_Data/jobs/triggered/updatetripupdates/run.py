import time
import updateprotobuf

# take this job 10 seconds out of phase with the transfer from BBB
time.sleep(10)

updateprotobuf.update('gtfs-rt-trip-updates', 'tripupdates.bin')
updateprotobuf.update('gtfs-rt-alerts', 'alerts.bin')
