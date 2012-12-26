'''
Created on Dec 17, 2012

@author: pidge
'''
#!/usr/bin/python

from config import *
from twisted.python import log
from Steps import Steps
from buildsteps import *
import ast
from buildsteps import *
from buildbot.process import factory as factory
from buildbot.steps.source import Git
from buildbot.schedulers.forcesched import ForceScheduler

class BuildSet():
    '''
    classdocs
    '''


    def __init__(self, name, layers, steps, builders):
        '''
        Constructor
        '''

        print "Creating BuildFactory for " + name + " buildset."
        locals()['f'+name] = factory.BuildFactory()
        
        for stepOrder in steps:
            for step in dict(stepOrder):
                if step=="CheckOutLayers":
                # All steps need the factory passed as the first param
                    print "Creating Checkout steps for " + name + "'s BuildSet."
                    factoryFN=getattr(locals()['f'+name], 'addStep')
                    for layer in dict(layers):
                        print "Adding step to checkout " + layers[layer][0]
                        factoryFN(Git(mode="clobber",
                                  repourl=layers[layer][0],
                                  branch='master',
                                  timeout=10000, retry=(5, 3)))    
                else:
                    print "Creating a " + step + " for " + name  + "'s BuildSet."
                    factoryFN=getattr(locals()['f'+name], 'addStep')
                    print 'these are kwargs: ' + str(stepOrder[step])
                    kwargs=stepOrder[step]
                    m = __import__ (step)
                    func = getattr(m, step)

                    factoryFN(func(locals()['f'+name], argdict=stepOrder[step]))
                    
        locals()['b%s' % name] = {'name': name,
                            'slavenames': [builders],
                            'builddir': name,
                            'factory': locals()['f'+name],
                            }
        yocto_builders=YOCTO_BUILDERS
        yocto_builders.append(locals()['b%s' % name])

