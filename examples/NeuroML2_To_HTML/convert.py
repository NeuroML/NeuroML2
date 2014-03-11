import lxml.etree as ET

import sys

try:
    infile = sys.argv[1]
except:
    print "Usage: convert.py _fileToConvert_"
    sys.exit(1)
    
xsl_file = 'NeuroML2_To_HTML.xsl'

dom = ET.parse(infile)
xslt = ET.parse(xsl_file)

transform = ET.XSLT(xslt)
newdom = transform(dom)
print(ET.tostring(newdom, pretty_print=True))
