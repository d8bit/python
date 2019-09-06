import sys
import os.path
import requests
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print 'File path needed'
    sys.exit(0)

filename = sys.argv[1]
if os.path.isfile(filename) == False:
    print 'File not found'
    sys.exit(0)

tree = ET.parse(filename)
root = tree.getroot()
for loc in root.iter('loc'):
    r = requests.get(loc.text)
    code = r.status_code
    if (code != 200):
        print 'Error on ',loc.text, code
    else:
        print loc.text
print 'Done'
