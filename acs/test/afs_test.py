#!/usr/bin/python

from acs.acs_utils import *
import acs.feature_afs as afs

import unittest

class AFSTest(unittest.TestCase):
    def setUp(self):
        self.log = ACSLog()
        self.acs = ACSUtils()

    def testAddFeature(self):
        """
        Install the AFS feature on the current cluster and verify it is working.
        """
        afs.addTo(self.acs)
        
        agents = self.acs.getAgentHostNames()
        for agent in agents:
            # docker volume create -d azurefile -o share=myshare --name=myvol
            # docker run -i -t -v myvol:/data busybox

            
if __name__ == '__main__':
    unittest.main()
