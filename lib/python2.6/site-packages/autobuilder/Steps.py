'''
Created on Dec 4, 2012

@author: pidge
'''


class Steps(object):

    def __init__(self):
        '''
        Constructor
        '''

    def checkoutLayers(self, factory, layers, branch="master"):
        from buildbot.steps.source import Git
        for layer in dict(layers):
            print "Adding step to checkout " + layers[layer][0]
            factory.addStep(Git(
                            mode="clobber",
                            repourl=layers[layer][0],
                            branch=branch,
                            timeout=10000, retry=(5, 3)))
    def buildImages(self):
        '''
        Constructor
        '''       
    def publishArtifacts(self):
        '''
        Constructor
        '''
    def helloWorld(self, factory, name, lastname):
        print "Hello " + name + " " + lastname
        '''
        Constructor
        '''