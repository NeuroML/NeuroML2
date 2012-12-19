###
#     Temporary script to test beta specification & examples.
#
#     Subject to change without notice!!!
###

import os
import sys
from lxml import etree
from urllib import urlopen

lems_def_dir="NeuroML2CoreTypes"
lems_def_list=os.listdir(lems_def_dir)

nml2_ex_dir="examples"
nml2_ex_list=os.listdir(nml2_ex_dir)

lems_schema = "../LEMS/Schemas/LEMS/LEMS_v0.6.xsd"
lems_schema_file = urlopen(lems_schema)

lems_xmlschema_doc = etree.parse(lems_schema_file)
lems_xmlschema = etree.XMLSchema(lems_xmlschema_doc)

nml2_schema = "Schemas/NeuroML2/NeuroML_v2beta.xsd"
nml2_schema_file = urlopen(nml2_schema)

nml2_xmlschema_doc = etree.parse(nml2_schema_file)
nml2_xmlschema = etree.XMLSchema(nml2_xmlschema_doc)

print "--------------------------------------------------"
print "    Validating LEMS files against: %s" %(lems_schema)

for file in lems_def_list:
    
    if file.endswith("xml") and not file.startswith("LEMS") and not file.startswith("Ex"):

        print "Validating %s..." %(file)

        doc = etree.parse(lems_def_dir+"/"+file)
        valid = lems_xmlschema.validate(doc)
        if valid:
            print "  It is valid!"
        else:
            print "  *** It's NOT valid! ***"

print "--------------------------------------------------"
print "    Validating NeuroML 2 files against: %s" %(nml2_schema)

for file in nml2_ex_list:

    if file.endswith("nml"):

        print "Validating %s..." %(file)

        doc = etree.parse(nml2_ex_dir+"/"+file)
        valid = nml2_xmlschema.validate(doc)
        if valid:
            print "  It is valid!"
        else:
            print "  *** It's NOT valid! ***"

print "--------------------------------------------------"
print "    Checking local copies of Schemas"

import filecmp

assert filecmp.cmp('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../neuroConstruct/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd')
assert filecmp.cmp('Schemas/NeuroML2/NeuroML_v2beta.xsd', '../neuroConstruct/NeuroML2/Schemas/NeuroML2/NeuroML_v2beta.xsd')

assert filecmp.cmp('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../libNeuroML/ideas/padraig/generatedFromV2Schema/regenerate/NeuroML_v2alpha.xsd')
assert filecmp.cmp('Schemas/NeuroML2/NeuroML_v2beta.xsd', '../libNeuroML/ideas/padraig/generatedFromV2Schema/regenerate/NeuroML_v2beta.xsd')

assert filecmp.cmp('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../org.neuroml.model/src/main/resources/Schemas/NeuroML2/NeuroML_v2alpha.xsd')
assert filecmp.cmp('Schemas/NeuroML2/NeuroML_v2beta.xsd', '../org.neuroml.model/src/main/resources/Schemas/NeuroML2/NeuroML_v2beta.xsd')

if '-r' in sys.argv:

    print "--------------------------------------------------"
    print "    Testing execution of LEMS files using jLEMS"

    import subprocess, os
    lems_def_list.sort()
    to_ignore = ['LEMS_NML2_Ex13_Instances.xml']
    for file in lems_def_list:

        if file.endswith("xml") and file.startswith("LEMS") and not file in to_ignore:

            lems_file = '%s/%s'%(lems_def_dir,file)
            print "Testing %s..." %(lems_file)

            #subprocess.call(['lems %s'%(lems_file)])
            #os.system('~/jLEMS/lems %s'%(lems_file))
            subprocess.call('~/jLEMS/lems %s &'%(lems_file), shell=True)
