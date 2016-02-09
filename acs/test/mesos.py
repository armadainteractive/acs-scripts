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
        self.log.debug("setUp the test environment")
        self.acs.marathonCommand('groups/azure?force=true', 'DELETE')

    def tearDown(self):
        self.log.debug("tearDown the test environment")
        self.acs.marathonCommand('groups/azure?force=true', 'DELETE')

    def getAppData(self):
        response = self.acs.marathonCommand('apps')
        self.log.debug(response)

        data = json.loads(response)
        return data["apps"]

    def deployApp(self):
        with open ('marathon-app.json', "r") as marathonfile:
            data=marathonfile.read().replace('\n', '').replace("\"", "\\\"")

        response = self.acs.marathonCommand('groups?force=True', 'POST', data)
        self.log.debug("deployment response: " + response)

    def testAppsAPI(self):
        """
        Check there are no apps installed on the cluster
        """
        apps = self.getAppData()
        self.assertEqual(len(apps),  0, "Should have no apps deployed. App count: " + str(len(apps)))

    @unittest.skip("Skip while we make testDeleteAPI work")
    def testDeploy(self):
        """Deploy a simple containerized application and verify it runs correctly."""

        self.deployApp()

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

    def testDeleteAPI(self):
        """
        Test that the delete API works
        """

        self.deployApp()

        apps = self.getAppData()
        app_count = len(apps)
        self.assertTrue(app_count >  1, "There are no apps deployed for us to delete")

        self.acs.marathonCommand('groups/azure?force=true', 'DELETE')

        apps = self.getAppData()
        self.assertTrue(len(apps) < app_count, "We failed to delete an application. Original app count: " + str(app_count) + " app count after deletion: " + str(len(apps)))

if __name__ == '__main__':
    unittest.main()
