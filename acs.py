#!/usr/bin/python

from acs.acs_utils import *
from acs.test.mesos import MesosTest
from acs.test.swarm import SwarmTest
from acs.test.afs_test import *

import optparse
import sys
import unittest
         
def main():
    """ACS command line tool"""

    usage = "usage: %prog [options] command\n\n"
    usage = usage + "Commands:\n\n"
    usage = usage + "deploy: deploy a cluster\n\n"
    usage = usage + "delete: delete a cluster\n\n"
    usage = usage + "test: test a cluster\n\n"
    usage = usage + "addFeature FEATURES: add one or mroe features to a cluster\n"
    usage = usage + "\tFEATURES is a comma separated list of features to add.\n\n"
    usage = usage + "env: display some useful information about the ACS environment currently configured"

    p = optparse.OptionParser(usage=usage, version="%prog 0.1")
    p.add_option('--config_file', '-c', default="cluster.ini",
                 help="define the configuration file to use. Default is 'cluster.ini'")
    options, arguments = p.parse_args()
 
    acs = ACSUtils(options.config_file)
    log = ACSLog()

    cmd = arguments[0]
    log.debug("Command: " + str(cmd))

    if cmd == "delete":
        acs.deleteResourceGroup()
    elif cmd == "deploy":
        acs.createDeployment()
        acs.addFeatures()
        print(acs.getEnvironmentSettings)
    elif cmd == "scale":
        acs.scale(arguments[1])
    elif cmd == "test":
        if arguments[1] == "deploy":
            mode = acs.getMode()
            log.debug("Testing deployment using mode: " + mode)
            if mode == "mesos":
                log.debug("Test Mesos mode")
                suite = unittest.TestLoader().loadTestsFromTestCase(MesosTest) 
                unittest.TextTestRunner(verbosity=2).run(suite) 
            elif mode == "swarm":
                log.debug("Test Swarm mode")
                test = SwarmTest(acs)
                test.testAll()
            else:
                log.error("Don't know how to test deployment mode: " + mode)
        elif arguments[1] == "feature":
            feature = arguments[2]
            if feature == "afs":
                log.debug("Test AFS Feature")
                test = AFSTest(acs)
                test.testAll()
            else: 
                log.error("Don't know how to test feature " + feature)
        else:
            log.error("Unrecognized testing profile")
    elif cmd == "addFeature":
        featureList = arguments[1]
        log.debug("Features: " + featureList)
        acs.addFeatures(featureList)
    elif cmd == "env":
        print(json.dumps(acs.getEnvironmentSettings(), indent=4))
    elif cmd == "docker":
        # Deprecated
        acs.agentDockerCommand(arguments[1])
    else:
        log.error("Unkown command: " + cmd)

if __name__ == '__main__':
    main()
