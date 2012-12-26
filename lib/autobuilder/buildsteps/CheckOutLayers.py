'''
Created on Dec 22, 2012

@author: pidge
'''
from buildbot.process.buildstep import LoggingBuildStep
from buildbot.steps.source import Git
from buildbot.status.results import SUCCESS, FAILURE


class CheckOutLayers(LoggingBuildStep):

    renderables = [ 'factory', 'layers', 'branch' ]

    def __init__(self, factory=None, layers=None, branch='master', **kwargs):
        LoggingBuildStep.__init__(self, **kwargs)
        self.factory = factory
        self.layers = layers
        self.branch = branch
        self.description = ["Checking", "out", "layers"]
        self.addFactoryArguments(factory=factory, layers=layers, branch=branch)

    def describe(self, done=False):
        return self.description

    def setStepStatus(self, step_status):
        LoggingBuildStep.setStepStatus(self, step_status)

    def start(self):
        try:
            for layer in dict(self.layers):
                print "Adding step to checkout " + self.layers[layer][0]
                self.factory.addStep(Git(
                                mode="clobber",
                                repourl=self.layers[layer][0],
                                branch=self.branch,
                                timeout=10000, retry=(5, 3)))    
            return self.finished(SUCCESS)
        except:
            return self.finished(FAILURE)
