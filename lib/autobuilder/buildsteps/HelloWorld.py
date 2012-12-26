'''
Created on Dec 22, 2012

@author: pidge
'''

from buildbot.steps.shell import ShellCommand

class HelloWorld(ShellCommand):
    haltOnFailure = True 
    flunkOnFailure = True 
    name = "Hello World" 
    def __init__(self, factory, argdict=None, **kwargs):
        self.firstname=""
        self.lastname=""
        self.factory = factory
        for k, v in argdict.iteritems():
            if k=="name":
                self.firstname=v
            elif k=="lastname":
                self.lastname=v
            else:
                setattr(self, k, v)
        self.description = "Hello World"
        self.command = "echo 'Hello World " + self.firstname + " " + self.lastname + "'"
        ShellCommand.__init__(self, **kwargs)

    def describe(self, done=False):
        description = ShellCommand.describe(self,done)
        return description

