###
#   Utility script to test current specification & examples. Subject to change without notice...
###

import os
from lxml import etree
from urllib import urlopen

lems_def_dir="NeuroML2CoreTypes"
lems_def_list=os.listdir(lems_def_dir)

nml2_ex_dir="examples"
nml2_ex_list=os.listdir(nml2_ex_dir)

lems_schema = "Schemas/LEMS/LEMS_v0.6.xsd"
lems_schema_file = urlopen(lems_schema)

lems_xmlschema_doc = etree.parse(lems_schema_file)
lems_xmlschema = etree.XMLSchema(lems_xmlschema_doc)

nml2_schema = "Schemas/NeuroML2/NeuroML_v2beta.xsd"
nml2_schema_file = urlopen(nml2_schema)

nml2_xmlschema_doc = etree.parse(nml2_schema_file)
nml2_xmlschema = etree.XMLSchema(nml2_xmlschema_doc)

for file in lems_def_list:
    
    if file.endswith("xml") and not file.startswith("LEMS") and not file.startswith("Ex"):

        print "Validating %s against %s" %(file, lems_schema)

        doc = etree.parse(lems_def_dir+"/"+file)
        valid = lems_xmlschema.validate(doc)
        if valid:
            print "  It is valid!"
        else:
            print "  *** It's NOT valid! ***"


for file in nml2_ex_list:

    if file.endswith("nml"):

        print "Validating %s against %s" %(file, nml2_schema)

        doc = etree.parse(nml2_ex_dir+"/"+file)
        valid = nml2_xmlschema.validate(doc)
        if valid:
            print "  It is valid!"
        else:
            print "  *** It's NOT valid! ***"