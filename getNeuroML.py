import os

import os.path as op
import subprocess

'''
try:
    from fabri3c.api import *
except ImportError as e:
    print "Problem loading Python module for Fabric"
'''

neuroml2_spec_repo = ['NeuroML/NeuroML2']
libneuroml_repo = ['NeuralEnsemble/libNeuroML']

java_neuroml_repos = ['NeuroML/org.neuroml.model.injectingplugin',
                      'NeuroML/org.neuroml.model',
                      'NeuroML/org.neuroml1.model',
                      'NeuroML/org.neuroml.export',
                      'NeuroML/org.neuroml.import',
                      'NeuroML/jNeuroML']


neuroml_repos = neuroml2_spec_repo + libneuroml_repo + java_neuroml_repos

jlems_repo = ['LEMS/jLEMS']
lems_spec_repos = ['LEMS/LEMS']
pylems_repos = ['LEMS/pylems']

java_repos = java_neuroml_repos + jlems_repo
lems_repos = jlems_repo + lems_spec_repos + pylems_repos

all_repos = neuroml_repos + lems_repos

# Set the prteferred method for cloning from GitHub
github_pref = "HTTP"
#github_pref = "SSH"
#github_pref = "Git Read-Only"

pre_gh={}
pre_gh["HTTP"]="https://github.com/"
pre_gh["SSH"]="git@github.com:"
pre_gh["Git Read-Only"]="git://github.com/"


def executeCommandInDir(command, directory):
    print ">> Executing: (%s) in dir: %s"%(command, directory)
    subprocess.call("cd %s; %s"%(directory, command), shell=True)

for repo in all_repos:
    print
    print "------ Updating: %s -------"%repo
    local_dir = ".."+os.sep+repo.split("/")[1]
    if not op.isdir(local_dir):
        command = "git clone %s%s"%(pre_gh[github_pref], repo)
        print "Creating a new directory: %s by cloning from GitHub"%(local_dir, command)
        executeCommandInDir(command, "..")

    executeCommandInDir("git pull", local_dir)
    if repo in java_repos:
        print "It's a Java repository, so installing using Maven"
        #executeCommandInDir("mvn install", local_dir)

