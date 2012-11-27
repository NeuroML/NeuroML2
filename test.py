###
#   Utility script to test current specification & examples. Subject to change without notice...
###

import os
from lxml import etree
from urllib import urlopen

def_dir="NeuroML2CoreTypes"
dirList=os.listdir(def_dir)

lems_schema = "Schemas/LEMS/LEMS_v0.6.xsd"
lems_schema_file = urlopen(lems_schema)

xmlschema_doc = etree.parse(lems_schema_file)
xmlschema = etree.XMLSchema(xmlschema_doc)

for file in dirList:
    

    if file.endswith("xml") and not file.startswith("LEMS") and not file.startswith("Ex"):

        print "Validating %s against %s" %(file, lems_schema)

        doc = etree.parse(def_dir+"/"+file)
        valid = xmlschema.validate(doc)
        if valid:
            print "  It is valid!"
        else:
            print "  *** It's NOT valid! ***"