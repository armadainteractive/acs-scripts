#!/usr/bin/python

from acs.acs_utils import ACSLog
from acs.acs_utils import ACSUtils

import json
import requests
import unittest
import sys
import time

class MesosTest(unittest.TestCase):
    def setUp(self):
        self.log = ACSLog()

    def testApps(self):
        """Check there are no apps installed on the cluster"""

        response = self.acs.marathonCommand('apps')
        
        data = json.loads(response)
        apps = data["apps"]

        self.assertEqual(len(apps),  0, "Should have no apps deployed")

    @unittest.skip("Skip deploy while we make the testAPI work")
    def testDeploy(self):
        """Deploy a simple containerized application and verify it runs correctly."""

        self.log.info("Deploy a two container app")
        with open ('marathon-app.json', "r") as marathonfile:
            data=marathonfile.read().replace('\n', '').replace("\"", "\\\"")

        self.log.debug(self.acs.marathonCommand('groups', 'POST', data))
        self.log.debug("End")

        url = "http://" + self.acs.getAgentsFQDN()
        self.log.debug("Check the application is running and accessible at " + url)
        for i in range (0,10):
            self.log.debug("Attempt to access service " + str(i) + " of 10")
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    self.log.debug("Got a 200 response from the application")
                    break
            except:
                e = sys.exc_info()[0]
                self.log.debug("Attempt failed: " + str(e))
                self.log.debug("Sleeping for 5 seconds")
                time.sleep (5)

        if i >= 9: 
            self.log.error("TESTING: Application never responded")
        self.log.info("End")

    @unittest.skip("Skip testDelete while we make testAPI work")
    def testDelete(self):
        """Test that the delete API works"""

        self.log.info("Remove the app")
        self.acs.marathonCommand('groups/azure?force=true', 'DELETE')
        self.log.info("End")

if __name__ == '__main__':
    unittest.main()
