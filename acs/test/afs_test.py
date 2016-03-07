from acs.acs_utils import ACSLog
import acs.feature_afs as afs

class AFSTest:
    def __init__(self, acs):
        self.acs = acs
        self.log = ACSLog()

    def testAll(self):
        self.testAddFeature()

    def testAddFeature(self):
        """
        Install the AFS feature on the current cluster and verify it is working.
        """
        afs.addTo(self.acs)

        agents = self.acs.getAgentHostNames()
        for agent in agents:
            cmd = "sudo initctl statsu azurefiles-dockervolumedriver"
            output = self.acs.executeOnAgent(cmd, agent)
            assertIsNotNone(output)
            self.log.debug("command output: " + output)
            
