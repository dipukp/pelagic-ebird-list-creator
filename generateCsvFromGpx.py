import xml.etree.ElementTree as ET
import sys

if len(sys.argv) != 2:
    print "Usage: generateCsvFromGpx.py <gpx-file>"
    quit()

tree = ET.parse(sys.argv[1])
print "time,lat,lon "
for elem in tree.iter():
    if "trkpt" in elem.tag:
        row = {}
        row["lat"] = elem.attrib["lat"]
        row["lon"] = elem.attrib["lon"]
        for child in elem:
            if "time" in child.tag:
                row["time"] = child.text
        print "%s,%s,%s" % (row["time"], row["lat"], row["lon"])
