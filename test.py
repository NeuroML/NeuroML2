###
#     Temporary script to test beta specification & examples.
#
#     Subject to change without notice!!!
###

import os
import sys
from lxml import etree
from urllib import urlopen

import subprocess
import filecmp
import unittest
import logging

lems_def_dir="NeuroML2CoreTypes"
lems_def_list=os.listdir(lems_def_dir)

lems_schema = "../LEMS/Schemas/LEMS/LEMS_v0.7.xsd"
lems_schema_file = urlopen(lems_schema)

lems_xmlschema_doc = etree.parse(lems_schema_file)
lems_xmlschema = etree.XMLSchema(lems_xmlschema_doc)

lems_ex_dir="../LEMS/examples"
lems_ex_list=os.listdir(lems_ex_dir)

nml2_schema = "Schemas/NeuroML2/NeuroML_v2beta.xsd"
nml2_schema_file = urlopen(nml2_schema)

nml2_xmlschema_doc = etree.parse(nml2_schema_file)
nml2_xmlschema = etree.XMLSchema(nml2_xmlschema_doc)

nml2_ex_dir="examples"
nml2_ex_list=os.listdir(nml2_ex_dir)

class TestValidateLEMSDefinitions(unittest.TestCase):
    def test_LEMS_definitions(self):
        print("Validating LEMS files against: {}".format(lems_schema))
        for file in lems_def_list:
            if file.endswith("xml") and not file.startswith("LEMS") and not file.startswith("Ex"):
                print("Validating {}...".format(file)),
                doc = etree.parse(lems_def_dir+"/"+file)
                valid = lems_xmlschema.validate(doc)
                self.assertTrue(valid, msg="{} is not valid!".format(file))

class TestValidateNeuroMLExamples(unittest.TestCase):
    def test_NeuroML_examples(self):
        print("Validating NeuroML 2 files against: {}".format(nml2_schema))
        for file in nml2_ex_list:
            if file.endswith("nml"):
                print("Validating {}...".format(file))
                #doc = etree.parse(nml2_ex_dir+"/"+file)
                #valid = nml2_xmlschema.validate(doc)
                exitVal = bool(subprocess.call(["jnml -validate "+ nml2_ex_dir+"/"+file], shell=True))
                self.assertTrue(exitVal, msg="{} is not valid!".format(file))

class TestLocalFilesInSync(unittest.TestCase):
    def checkSameFile(self, fileA, fileB):
        print "Comparing {} to {}".format(fileA, fileB)
        return filecmp.cmp(fileA, fileB)
    def test_NeuroML_schemas_libNeuroML(self):
        self.assertTrue(self.checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',
                                           '../libNeuroML/neuroml/nml/NeuroML_v2beta.xsd'),
                        msg="NeuroML schemas in libNeuroML not in sync!")
    def test_NeuroML_schemas_org_neuroml_model(self):
        self.assertTrue(self.checkSameFile('Schemas/NeuroML2/NeuroML_v2alpha.xsd',
                                           '../org.neuroml.model/src/main/resources/Schemas/NeuroML2/NeuroML_v2alpha.xsd'),
                        msg="NeuroML alpha schemas in org.neuroml.model not in sync!")
        self.assertTrue(self.checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',
                                           '../org.neuroml.model/src/main/resources/Schemas/NeuroML2/NeuroML_v2beta.xsd'),
                        msg="NeuroML beta schemas in org.neuroml.model not in sync!")
    def test_NeuroML_schemas_Cvapp_NeuroMorpho(self):
        neuromorpho_not_present = not os.path.isdir('../Cvapp-NeuroMorpho.org')
        self.assertTrue(neuromorpho_not_present or self.checkSameFile('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../Cvapp-NeuroMorpho.org/Schemas/NeuroML2/NeuroML_v2alpha.xsd'),
                        msg="NeuroML alpha schemas in Cvapp-NeuroMorpho.org not in sync!")
        self.assertTrue(neuromorpho_not_present or self.checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',  '../Cvapp-NeuroMorpho.org/Schemas/NeuroML2/NeuroML_v2beta.xsd'),
                        msg="NeuroML beta schemas in Cvapp-NeuroMorpho.org not in sync!")
    def test_NeuroML_schemas_neuroConstruct(self):
        neuroConstruct_not_present = not os.path.isdir('../neuroConstruct')
        self.assertTrue(neuroConstruct_not_present or self.checkSameFile('Schemas/NeuroML2/NeuroML_v2alpha.xsd', '../neuroConstruct/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd'),
                        msg="NeuroML alpha schemas in neuroConstruct not in sync!")
        self.assertTrue(neuroConstruct_not_present or self.checkSameFile('Schemas/NeuroML2/NeuroML_v2beta.xsd',  '../neuroConstruct/NeuroML2/Schemas/NeuroML2/NeuroML_v2beta.xsd'),
                        msg="NeuroML beta schemas in neuroConstruct not in sync!")
    def test_NeuroML_comp_types_org_neuroml_model(self):
        are_files_identical_list = []
        for filename in lems_def_list:
            if filename.endswith("xml") and not filename.startswith("Ex"):
                main_def = lems_def_dir+"/"+filename
                copy_org_neuroml_model = "../org.neuroml.model/src/main/resources/"+lems_def_dir+"/"+filename
                are_files_identical_list.append(self.checkSameFile(main_def, copy_org_neuroml_model))
        self.assertTrue(all(are_files_identical_list),
                        msg="NeuroML core component types definitions in org.neuroml.model are not in sync!")
    def test_NeuroML_examples_org_neuroml_model(self):
        are_files_identical_list = []
        for filename in nml2_ex_list:
            if filename.endswith("nml"):
                main_ex = nml2_ex_dir+"/"+filename
                copy_org_neuroml_model = "../org.neuroml.model/src/main/resources/"+nml2_ex_dir+"/"+filename
                are_files_identical_list.append(self.checkSameFile(main_ex, copy_org_neuroml_model))
        self.assertTrue(all(are_files_identical_list),
                        msg="NeuroML examples in org.neuroml.model are not in sync!")
    def test_LEMS_examples_jLEMS(self):
        are_files_identical_list = []
        for filename in lems_ex_list:
            if filename.endswith("xml"):
                main_ex = lems_ex_dir+"/"+filename
                copy_jLEMS = "../jLEMS/src/test/resources/"+filename
                are_files_identical_list.append(self.checkSameFile(main_ex, copy_jLEMS))
        self.assertTrue(all(are_files_identical_list),
                        msg="LEMS examples in jLEMS are not in sync!")
    def test_LEMS_examples_pylems(self):
        are_files_identical_list = []
        for filename in lems_ex_list:
            if filename.endswith("xml"):
                main_ex = lems_ex_dir+"/"+filename
                copy_pylems = "../pylems/examples/"+filename
                are_files_identical_list.append(self.checkSameFile(main_ex, copy_pylems))
        self.assertTrue(all(are_files_identical_list),
                        msg="LEMS examples in pylems are not in sync!")


if __name__ == '__main__':
    unittest.main()

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
                subprocess.call('jnml %s -nogui &'%(lems_file), shell=True)
